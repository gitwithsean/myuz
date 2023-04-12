from django.core.management.base import BaseCommand
from importlib import import_module


class Command(BaseCommand):
    help = 'Execute a method from a module in a Django app directory'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str, help='Name of the Django app directory')
        parser.add_argument('module', type=str, help='Name of the module with the method to execute')

    def handle(self, *args, **options):
        app_name = options['app']
        module_name = options['module']

        try:
            module = import_module(f"{app_name}.{module_name}")
            module.test_from_manager()
        except ModuleNotFoundError:
            self.stderr.write(f"Module '{module_name}' not found within '{app_name}'")
        except AttributeError:
            self.stderr.write(f"Method test_from_manager() not found within module '{module_name}' within app '{app_name}'- please add it to the module")