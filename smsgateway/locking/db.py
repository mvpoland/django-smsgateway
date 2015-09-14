# -*- coding: utf-8 -*-
from __future__ import absolute_import
from locking.exceptions import AlreadyLocked
from locking.models import NonBlockingLock, MAX_AGE_FOREVER
from logging import getLogger


logger = getLogger(__name__)


class Lock(object):

    def __init__(self, name):
        self.name = name
        self.lock = None

    def acquire(self, timeout):
        if timeout < 0:
            # django-smsgateway by default uses a negative value to indicate the lock should be acquired until it's
            # released. Django-locking does not support negative values.
            timeout = MAX_AGE_FOREVER
        try:
            self.lock = NonBlockingLock.objects.acquire_lock(None, timeout, self.name)
            return True
        except AlreadyLocked:
            logger.info('Could not acquire lock %s', self.name)
            return False

    def release(self):
        self.lock.release()
