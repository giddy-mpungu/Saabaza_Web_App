from django.core import management

import appsaabaza


class Command(management.BaseCommand):
    help = 'Display version information.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--build-string', action='store_true', dest='build_string',
            help='Show build string.',
        )

    def handle(self, *args, **options):
        if options['build_string']:
            self.stdout.write('{}\n'.format(appsaabaza.__build_string__))
        else:
            self.stdout.write('{}\n'.format(appsaabaza.__version__))
