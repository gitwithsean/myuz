import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Dumps data from all models in all apps to JSON files'

    def handle(self, *args, **options):
        for app in apps.get_app_configs():
            try:
                # Create the 'fixtures' directory if it doesn't exist
                fixtures_dir = os.path.join(app.path, "fixtures")
                if not os.path.exists(fixtures_dir):
                    os.makedirs(fixtures_dir)

                # Dump data for all models in the app
                for model in app.get_models():
                    model_name = model.__name__.lower()
                    output_file = os.path.join(fixtures_dir, f"{model_name}.json")
                    call_command("dumpdata", f"{app.label}.{model_name}", "--indent", "4", "--output", output_file)
                    self.stdout.write(self.style.SUCCESS(f"Dumped data for model '{app.label}.{model_name}' to '{output_file}'"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to dump data for app '{app.label}': {e}"))
