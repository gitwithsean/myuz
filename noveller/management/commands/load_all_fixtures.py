from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Loads all fixtures for all apps in the project'

    def handle(self, *args, **options):
        for app in apps.get_app_configs():
            try:
                # Load fixtures for the app
                fixture_path = f"{app.path}/fixtures"
                call_command("loaddata", fixture_path, verbosity=1)
                self.stdout.write(self.style.SUCCESS(f"Loaded fixtures for app '{app.label}'"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to load fixtures for app '{app.label}': {e}"))
