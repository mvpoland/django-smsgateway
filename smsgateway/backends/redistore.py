# -*- encoding: utf-8 -*-
from datetime import datetime
from hashlib import md5
from logging import getLogger
from redis import ConnectionPool, Redis

from django.conf import settings

from smsgateway.enums import DIRECTION_OUTBOUND
from smsgateway.models import SMS
from smsgateway.backends.base import SMSBackend
from smsgateway.sms import SMSRequest


logger = getLogger(__name__)

OUTGOING_SMS_EXPIRE_SECONDS = getattr(
    settings, 'SMSGATEWAY_OUTGOING_SMS_EXPIRE_SECONDS', 0
)


class RedistoreBackend(SMSBackend):

    def __init__(self):
        self.redis_key_prefix = None
        self.redis_pool = None
        self.redis_conn = None
        self.reference = None
        self.sender = None
        self.sms_data_iter = None
        self.sent_smses = []

    def prefix(self, key):
        return '{}{}'.format(self.redis_key_prefix, key)

    def _initialize(self, sms_request, account_dict):
        sms_list = self._get_sms_list(sms_request)
        if not len(sms_list):
            logger.error('Nothing to send. sms_request: {}'.format(sms_request))
            return False

        if sms_request.signature:
            self.sender = sms_request.signature
        else:
            self.sender = '[{}]'.format(self.get_slug())

        self.sms_data_iter = SMSDataIterator(sms_list, account_dict)

        self._initialize_redis_pool(account_dict)

        return True

    def _initialize_redis_pool(self, account_dict):
        host = account_dict['host'] or 'localhost'
        port = account_dict['port'] or 6379
        self.redis_key_prefix = account_dict['key_prefix']
        self.redis_pool = ConnectionPool(
            host=host,
            port=port,
            db=account_dict['dbn'],
            password=account_dict['pwd']
        )

    def get_send_reference(self, sms_request):
        return '+'.join([
            str(datetime.now().strftime('%Y%m%d%H%M%S')),
            ''.join(sms_request.to[:1]),
            str(sms_request.msg),
        ])

    def _get_sms_list(self, sms_request):
        if not sms_request:
            return []
        sms_list = []

        self.reference = self.get_send_reference(sms_request)
        self.reference = md5(self.reference.encode()).hexdigest()

        for msisdn in sms_request.to:
            sms_list.append(
                SMSRequest(
                    msisdn,
                    sms_request.msg,
                    sms_request.signature,
                    reliable=sms_request.reliable,
                    reference=self.reference
                )
            )
        return sms_list

    def _send_smses(self):
        if not self.sms_data_iter:
            return []

        pipe = self.redis_conn.pipeline(transaction=False)
        key = self.reference
        queue_key = self.prefix('smsreq:{}'.format(key))
        allqueues_key = self.prefix('outq')

        # feed the pipe
        for idx, sms_data in enumerate(self.sms_data_iter):
            source_sms = sms_data.pop('source_sms')
            sms_key = self.prefix('sms:{}:{}'.format(key, idx))
            pipe.hmset(sms_key, sms_data)
            if OUTGOING_SMS_EXPIRE_SECONDS:
                pipe.expire(sms_key, OUTGOING_SMS_EXPIRE_SECONDS)
            pipe.rpush(queue_key, sms_key)
            sent_sms = {
                'sender': self.sender,
                'to': sms_data['destination_addr'],
                'content': source_sms.msg,
                'backend': self.get_slug(),
                'direction': DIRECTION_OUTBOUND,
                'gateway_ref': source_sms.reference
            }
            self.sent_smses.append(sent_sms)
        pipe.lpush(allqueues_key, queue_key)

        # execute the pipe
        pipe_results = pipe.execute()

        # split results into chunks for each SMS (last will be a result of lpush)
        results_per_sms = 3 if OUTGOING_SMS_EXPIRE_SECONDS else 2
        pipe_results = [pipe_results[i:i + results_per_sms]
                        for i in range(0, len(pipe_results), results_per_sms)]

        return pipe_results[:-1], pipe_results[-1]

    def _check_sent_smses(self, results):
        """Check pipe execution results and create SMS objects."""
        sms_results, lpush_result = results
        if not sms_results:
            return False

        for counter, result in enumerate(sms_results, start=1):
            created, listlen = result[0], result[-1]
            instance_data = self.sent_smses.pop(0)
            if created and listlen == counter:
                SMS.objects.create(**instance_data)

        return True if lpush_result[0] else False

    def send(self, sms_request, account_dict):
        """RedistoreBackend Entry Point"""
        self._initialize(sms_request, account_dict)
        self.redis_conn = Redis(connection_pool=self.redis_pool)
        redis_results = self._send_smses()
        check_result = self._check_sent_smses(redis_results)
        return check_result

    def get_slug(self):
        return 'redistore'

    def maintenance_cleanup(self, account_dict):
        """
        Perform maintenance cleanup of obsolete messages.

        This method is responsible for cleaning up messages that were not processed
        due to errors, breakdowns, or messages that got stuck in the system. It ensures
        that the system remains clean and free of outdated or problematic messages.

        :param dict account_dict: account information needed to initialize the redis pool

        Note:
        The "subq" queue is an internal redis queue of the "smpp-esme" service.
        We reference it here to have a single place responsive for all queues cleanups.
        """
        self._initialize_redis_pool(account_dict)

        redis_conn = Redis(connection_pool=self.redis_pool)
        subq_queue_name = self.prefix("subq")
        records = redis_conn.lrange(subq_queue_name, 0, -1)
        records = [r.decode("utf-8") if isinstance(r, bytes) else r for r in records]
        removed = []
        for record in records:
            if not redis_conn.exists(record):
                redis_conn.lrem(name=subq_queue_name, value=record, num=1)
                removed.append(record)

        removed_count = len(removed)
        remaining_count = len(records) - removed_count
        logger.info("Cleared %d records from 'subq' queue, remaining: %d",
                    removed_count, remaining_count)


class SMSDataIterator:
    def __init__(self, sms_list, account_dict):
        self.sms_list = sms_list
        self.source_addr_ton = account_dict['source_addr_ton']
        self.source_addr = account_dict['source_addr']
        self.dest_addr_ton = account_dict['dest_addr_ton']

    def __iter__(self):
        return self

    def __next__(self):
        while len(self.sms_list):
            sms = self.sms_list.pop(0)
            text = sms.msg
            text = text.replace('€', 'EUR')
            text = text.encode('iso-8859-1', 'replace')

            return {
                'source_addr_ton': self.source_addr_ton,
                'source_addr': self.source_addr,
                'dest_addr_ton': self.dest_addr_ton,
                'destination_addr': sms.to[0],
                'short_message': text,
                'esme_vrfy_seqn': -1,
                'source_sms': sms
             }
        raise StopIteration
