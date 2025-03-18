from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from smsgateway.models import SMS, QueuedSMS


class SMSAdmin(admin.ModelAdmin):
    list_display = ('direction', 'sent', 'sender', 'to', 'content', 'operator', 'backend', 'gateway', 'gateway_ref')
    search_fields = ('sender', 'to', 'content',)
    list_filter = (
        (
            "sent", DateRangeFilterBuilder(title="By Sent date"),
        ),
        'operator', 'direction', 'gateway', 'backend',
    )


admin.site.register(SMS, SMSAdmin)


class QueuedSMSAdmin(admin.ModelAdmin):
    list_display = ('to', 'content', 'created', 'using', 'priority')
    search_fields = ('to', 'content')
    list_filter = ('created', 'priority', 'using')


admin.site.register(QueuedSMS, QueuedSMSAdmin)
