from django.core.management.base import BaseCommand

from smsgateway.tasks import run_maintenance_cleanup


class Command(BaseCommand):
    help = 'Run maintenance cleanup task.'

    def add_arguments(self, parser):
        parser.add_argument('--backend', help='Slug of the backend')
        parser.add_argument('--account', help='Slug of the account')

    def handle(self, *args, **options):        
        run_maintenance_cleanup(
            backend_slug=options['backend'],
            account_slug=options['account'],
        )
