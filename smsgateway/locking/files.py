# -*- coding: utf-8 -*-
from __future__ import absolute_import
from lockfile import FileLock, AlreadyLocked, LockTimeout
from logging import getLogger


logger = getLogger(__name__)


class Lock(object):

    def __init__(self, name):
        self.name = name
        self.lock = None

    def acquire(self, timeout):
        self.lock = FileLock(self.name)
        try:
            self.lock.acquire(timeout)
            return True
        except AlreadyLocked:
            logger.info('Could not acquire lock %s', self.name)
            return False
        except LockTimeout:
            logger.info('Lock %s timed out', self.name)
            return False

    def release(self):
        self.lock.release()
