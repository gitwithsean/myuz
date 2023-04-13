from django.core.management.base import BaseCommand
from importlib import import_module
from phusis.models import *
class Command(BaseCommand):
    help = 'Execute a method from a script in a Django app directory'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str, help='Name of the Django app directory')
        parser.add_argument('path_to_script', type=str, help='Path of the script with the method to execute')

    def handle(self, *args, **options):
        app_name = options['app']
        path_to_script = options['path_to_script']

        import_module(f"{app_name}.{path_to_script}").test_from_manager(*args)
