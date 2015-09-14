import os
import sys


def setup_django_settings():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, os.getcwd())
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


def run_tests():
    if not os.environ.get('DJANGO_SETTINGS_MODULE', False):
        setup_django_settings()

    import django
    from django.test.runner import DiscoverRunner

    django.setup()

    test_suite = DiscoverRunner(verbosity=2, interactive=True, failfast=False)
    test_suite.run_tests(['smsgateway'])


if __name__ == '__main__':
    run_tests()
