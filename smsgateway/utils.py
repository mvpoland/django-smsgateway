import logging
import re

from django.conf import settings
from smsgateway.enums import WHITELIST

logger = logging.getLogger(__name__)


SMS_LENGTH_LIMIT = getattr(settings, 'SMSGATEWAY_SMS_LENGTH_LIMIT', 160)


def strspn(source, allowed):
    newchrs = []
    for c in source:
        if c in allowed:
            newchrs.append(c)
    return u''.join(newchrs)


def check_cell_phone_number(number):
    cleaned_number = strspn(number, u'0123456789')
    msisdn_prefix = getattr(settings, 'SMSGATEWAY_MSISDN_PREFIX', '')
    if msisdn_prefix and not cleaned_number.startswith(msisdn_prefix):
        cleaned_number = msisdn_prefix + cleaned_number
    return str(cleaned_number)


def truncate_sms(text, max_length=SMS_LENGTH_LIMIT):
    text = text.strip()
    if len(text) <= max_length:
        return text
    else:
        logger.error("Trying to send an SMS that is too long: %s", text)
        return text[:max_length-3] + '...'


def parse_sms(content):

    # work with uppercase and single spaces
    content = content.upper().strip()
    content = re.sub('\s+', " ", content)

    from smsgateway.backends.base import hook
    for keyword, subkeywords in hook.iteritems():
        if content[:len(keyword)] == unicode(keyword):
            remainder = content[len(keyword):].strip()
            if '*' in subkeywords:
                parts = remainder.split(u' ')
                subkeyword = parts[0].strip()
                if subkeyword in subkeywords:
                    return [keyword] + parts
                return keyword, remainder
            else:
                for subkeyword in subkeywords:
                    if remainder[:len(subkeyword)] == unicode(subkeyword):
                        subremainder = remainder[len(subkeyword):].strip()
                        return [keyword, subkeyword] + subremainder.split()
    return None


def should_send(msisdn):
    return WHITELIST is None or str(msisdn) in WHITELIST
