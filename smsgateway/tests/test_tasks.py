from redis import ConnectionPool, Redis

from django.test import TestCase
from django.utils import timezone

from smsgateway import get_account
from smsgateway.models import SMS
from smsgateway.tasks import recv_smses, _send_smses


def _receive_sms_from_esme(textmsg, recipient):
    racc = get_account("redistore")

    def redis_prefix(key):
        return '%s%s' % (racc['key_prefix'], key)

    received = timezone.now()
    sender = "P4"
    message_md5 = "fake"
    sms_data = {
        'sent': "%s" % received,
        'content': textmsg,
        'sender': sender,
        'to': recipient,
        'operator': 0,
        'gateway_ref': message_md5,
        'backend': 'redistore'
    }
    smsk = "sms:%s" % sms_data["gateway_ref"]

    rpool = ConnectionPool(
        host=racc['host'], port=racc['port'], db=racc['dbn'], password=racc['pwd']
    )
    rconn = Redis(connection_pool=rpool)

    rconn.hmset(redis_prefix(smsk), sms_data)
    rconn.rpush(redis_prefix('inq'), redis_prefix(smsk))


class RecvSmsesTestCase(TestCase):
    def test_success(self):
        # arrange
        textmsg = "good job"
        recipient = "234"
        _receive_sms_from_esme(textmsg, recipient)

        # act
        recv_smses()

        # assert
        smses = SMS.objects.all()
        self.assertEqual(smses.count(), 1)
        sms = smses[0]
        self.assertEqual(sms.to, recipient)
        self.assertEqual(sms.content, textmsg)
        self.assertEqual(sms.sender, "P4")


class SendSmsesTestCase(TestCase):
    def test_success(self):
        _send_smses()
