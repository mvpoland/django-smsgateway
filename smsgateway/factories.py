# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import object
import factory
from factory.django import DjangoModelFactory
from smsgateway.models import SMS


class SMSFactory(DjangoModelFactory):
    class Meta(object):
        model = SMS

    content = 'This is a test'
    sender = factory.Sequence(lambda n: u'+32476{0:06d}'.format(n))
    to = factory.Sequence(lambda n: u'+32476{0:06d}'.format(n))
