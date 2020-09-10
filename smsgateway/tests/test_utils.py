from django.test import TestCase

from smsgateway.utils import check_cell_phone_number, parse_sms


class CheckNumberTest(TestCase):
    def test_international_format(self):
        return check_cell_phone_number('+32478123456') == '32478123456'

    def test_international_format_without_plus(self):
        return check_cell_phone_number('32478123456') == '32478123456'

    def test_national_format(self):
        return check_cell_phone_number('0478123456') == '32478123456'

    def test_national_format_without_leading_zero(self):
        return check_cell_phone_number('478123456') == '32478123456'


class ParseSMSTestCase(TestCase):
    def test_not_matched_any_hook(self):
        # arrange
        content = "aa            aa      "

        # act
        parsed_content = parse_sms(content)

        # arrange
        self.assertEqual(parsed_content, ("TOPUP NOLIMIT", ""))

    def test_matched_topup(self):
        # arrange
        content = "topup      NoLiMiT   szybko"

        # act
        parsed_content = parse_sms(content)

        # arrange
        self.assertEqual(parsed_content, ("TOPUP NOLIMIT", "SZYBKO"))
