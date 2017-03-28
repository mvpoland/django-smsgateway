# Test settings
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory;'
    }
}
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'smsgateway',
)

# Necessary for creating docs
SECRET_KEY = 'asfhasdlfjh'
MEDIA_CACHE_DIR = '.'
MEDIA_CACHE_URL = '/media'
