from django.core.management.base import BaseCommand
from importlib import import_module


class Command(BaseCommand):
    help = 'python manage.py load_data_from_dir_into_db [app] [dir_to_jsons]'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str, help='Name of the Django app directory')
        parser.add_argument('dir_to_jsons', type=str, help='Directory to location of json files')

    def handle(self, *args, **options):
        app_name = options['app']
        dir_to_jsons = options['dir_to_jsons']

        for file in dir_to_jsons:
            pass