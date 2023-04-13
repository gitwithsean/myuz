import os
from django import forms
from django.core.management.base import BaseCommand
from django.apps import apps
from djangojsonschema.jsonschema import DjangoFormToJSONSchema
import json

class Command(BaseCommand):
    help = "Generate JSON schemas for all tables in the SQLite database and save them to the target directory"

    def add_arguments(self, parser):
        parser.add_argument('app', type=str, help="The name of the Django app")
        parser.add_argument('target_dir', type=str, help="The target directory to save JSON schema files")

    def create_model_form(self, mo):
        class ModelForm(forms.ModelForm):
            class Meta:
                model = mo
                fields = '__all__'

        return ModelForm

    def handle(self, *args, **options):
        app_name = options['app']
        target_dir = options['target_dir']

        # Ensure the target directory exists
        os.makedirs(target_dir, exist_ok=True)

        # Get all models in the app
        app = apps.get_app_config(app_name)
        models = app.get_models()

        # Generate JSON schemas for each model and save them to the target directory
        for model in models:
            model_name = model.__name__
            form_class = self.create_model_form(model)
            
            # If you are running python 3, the below command will fail
            # iteritems() method not being available in Python 3. In Python 3, 
            # you can use the items() method instead. Update the djangojsonschema 
            # package's jsonschema.py file to use the items() method:
            
            # * Open the jsonschema.py file in your text editor. You can 
            # find the file in your  site-packages directory. The path 
            # should look like this: 
            # ~/.local/lib/python3.10/site-packages/djangojsonschema/jsonschema.py

            # Replace the following line (should be line 21):
            # for name, field in form.base_fields.iteritems():
            # for name, field in form.base_fields.items():

            try:
                schema = DjangoFormToJSONSchema().convert_form(form_class)
            except:
                print("If your code has failed at this point it is likely because in python3 iteritems() method is not available. BUT, it's ok, you can use the items() method instead. Update the djangojsonschema package's jsonschema.py file to use the items() method:\n\n * Open the jsonschema.py file in your text editor. You can find the file in your  site-packages directory. The path hould look like this: \n\n~/.local/lib/python3.10/site-packages/djangojsonschema/jsonschema.py\n\n* Replace the following line (should be line 21:\n\nfor name, field in form.base_fields.iteritems():\n\nfor name, field in form.base_fields.items():")
                
            file_name = f"{model_name}.json"
            file_path = os.path.join(target_dir, file_name)

            with open(file_path, 'w') as f:
                json.dump(schema, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"JSON schemas generated and saved to {target_dir}"))
