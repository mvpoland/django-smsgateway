## Changelog

### 3.1.3
- Added requirement `django-admin-rangefilter==0.13.2`
- Added sent date range filter to SMSAdmin's list filter
- Removed date_hierarchy from SMSAdmin
- Fix missing quote in `smsgateway/backends/kpnbe.py`

### 3.1.2

- Added configurable Redis expiration timeouts for incoming/outgoing messages.
- Added `run_maintenance_cleanup` task to remove obsolete messages.

### 3.0.1

- Renamed smsgateway.tasks.recv_smses param `async` to `run_async`.
- Dropped future and six references.

## Installation

How to install:

* Add 'smsgateway' to your INSTALLED_APPS
* Add 'rangefilter' to your INSTALLED_APPS due to changes in `3.1.3` version
* Configure it:

    # settings.py

    # This is where your incoming messages will be handled by your web app.
    SMSGATEWAY_HOOK = {'MV': 'mvne.activation.utils.incoming_sms',
                       'SIM': 'mvne.activation.utils.incoming_sms'}

    # This is a list of accounts of SMS gateway providers.
    SMSGATEWAY_ACCOUNTS = {
        '__default__': 'mobileweb', # This is your default account. You MUST specify this! It points to one of your accounts below this line.
        'mobileweb': {'backend': 'mobileweb', 'username': 'johndoe', 'password': '12345678', 'sid': '413'}, # Example account
        'smsextrapro': {'backend': 'smsextrapro', 'username': 'johndoe', 'password': '87654321'}, # Example account
    }

    # This is where you set up the backends in use. You can use your own too! Please look at the built-in backends for an example.
    SMSGATEWAY_BACKENDS = (
        'smsgateway.backends.mobileweb.MobileWebBackend',
        'smsgateway.backends.smsextrapro.SmsExtraProBackend',
    )

* Some backends support incoming text messages:

    # urls.py

    from smsgateway import backends

    urlpatterns = ('',
        (r'^incoming_sms/$', backends.get_backend('mobileweb').handle_incoming),
    )

* Set up your SMS gateway to use this url for incoming messages.