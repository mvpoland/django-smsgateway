# -*- encoding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory
from smsgateway.models import SMS


class SMSFactory(DjangoModelFactory):
    class Meta:
        model = SMS

    content = 'This is a test'
    sender = factory.Sequence(lambda n: '+32476{0:06d}'.format(n))
    to = factory.Sequence(lambda n: '+32476{0:06d}'.format(n))
