from django.test import TestCase

from smsgateway import send


class SendSMSTestCase(TestCase):
    def test_success(self):
        # arrange
        msisdn = "48732007007"
        msg = "Hello world!1"
        sms_signature = "Vikingi"
        reliable = False

        # act
        result = send(msisdn, msg, sms_signature, reliable=reliable)

        # assert
        self.assertTrue(result)
