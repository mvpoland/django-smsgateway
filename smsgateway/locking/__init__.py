# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf import settings
from django.utils.module_loading import import_string


def acquire_lock(name, timeout):
    classname = getattr(settings, 'SMSGATEWAY_LOCKING_CLASS', 'smsgateway.locking.files.Lock')
    lock_class = import_string(classname)
    lock = lock_class(name)
    lock.acquire(timeout)
    return lock
