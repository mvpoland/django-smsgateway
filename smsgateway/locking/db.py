# -*- coding: utf-8 -*-
from __future__ import absolute_import
from locking.exceptions import AlreadyLocked
from locking.models import NonBlockingLock
from logging import getLogger


logger = getLogger(__name__)


class Lock(object):

    def __init__(self, name):
        self.name = name
        self.lock = None

    def acquire(self, timeout):
        try:
            self.lock = NonBlockingLock.objects.acquire_lock(None, timeout, self.name)
            return True
        except AlreadyLocked:
            logger.info('Could not acquire lock %s', self.name)
            return False

    def release(self):
        self.lock.release()
