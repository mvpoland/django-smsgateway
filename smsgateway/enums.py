from django.utils.translation import gettext_lazy

OPERATOR_UNKNOWN = 0
OPERATOR_PROXIMUS = 1
OPERATOR_MOBISTAR = 2
OPERATOR_BASE = 3
OPERATOR_OTHER = 999
OPERATOR_CHOICES = (
    (OPERATOR_UNKNOWN, gettext_lazy('Unknown')),
    (OPERATOR_PROXIMUS, 'Proximus'),
    (OPERATOR_MOBISTAR, 'Mobistar'),
    (OPERATOR_BASE, 'Base'),
    (OPERATOR_OTHER, gettext_lazy('Other')),
)

GATEWAY_MOBILEWEB = 1
GATEWAY_SMSEXTRAPRO = 3
GATEWAY_SPRYNG = 4
GATEWAY_CHOICES = (
    (GATEWAY_MOBILEWEB, 'MobileWeb'),
    (GATEWAY_SMSEXTRAPRO, 'SmsExtraPro'),
    (GATEWAY_SPRYNG, 'Spryng'),
)

DIRECTION_BOTH = 2
DIRECTION_INBOUND = 1
DIRECTION_OUTBOUND = 0
DIRECTION_CHOICES = (
    (DIRECTION_BOTH, gettext_lazy('Both')),
    (DIRECTION_INBOUND, gettext_lazy('Inbound')),
    (DIRECTION_OUTBOUND, gettext_lazy('Outbound')),
)

PRIORITY_HIGH = '1'
PRIORITY_MEDIUM = '2'
PRIORITY_LOW = '3'
PRIORITY_DEFERRED = '9'

PRIORITIES = (
    (PRIORITY_HIGH,     'high'),
    (PRIORITY_MEDIUM,   'medium'),
    (PRIORITY_LOW,      'low'),
    (PRIORITY_DEFERRED, 'deferred'),
)
