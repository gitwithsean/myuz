import json, os
from django.core.management.base import BaseCommand
from django.apps import apps
import inflect
from phusis.models import *
from pprint import pprint

def create_related_objects(model_name, related_obj_name, related_objs, main_obj):
    model = apps.get_model(f'phusis.{model_name}')
    related_model = apps.get_model(f'phusis.{related_obj_name}')
    related_objs = [
        related_model(**related_obj)
        for related_obj in related_objs
    ]
    related_objs = related_model.objects.bulk_create(related_objs)
    getattr(main_obj, related_obj_name).set(related_objs)

def convert_filename_to_classname(filename):
    
    # The next lines of code takes a filename string like 
    # (init_class_names.json and turn it into ClassNames)
    class_name = os.path.splitext(filename)[0]
    class_name_parts = class_name[5:].split('_')
    class_name = ''.join([part.capitalize() for part in class_name_parts])
    
    #This will make it singular
    p = inflect.engine()
    if p.singular_noun(class_name):
        return p.singular_noun(class_name)
    else:
        return class_name

def init_objects(model_name, objects):
    model = apps.get_model(f'phusis.{model_name}')
    for obj in objects:
        for att_name, att_value in obj.items():
            if isinstance(att_value, list):
                related_objs = obj.pop(att_name, [])
                main_obj = model.objects.create(**obj)
                create_related_objects(model_name, att_name, related_objs, main_obj)
            else:
                setattr(obj, att_name, att_value)
        model.objects.create(**obj)

class Command(BaseCommand):
    help = "Loads data in {app_name}/init_data/*.json into the database"
    
    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help="The name of the Django app")

    def handle(self, *args, **options):
        app_name = options['app_name']
        self.load_init_data(app_name)
    
    def load_init_data(self, app_name):
        init_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'init_data')

        for filename in os.listdir(f"{app_name}/init_data/"):
            if not filename.endswith('.json'):
                continue

            with open(os.path.join(f"{app_name}/init_data/", filename), 'r') as f:
                data = json.load(f)
                if 'all_class_types' in data:
                    for each in data['all_class_types']:
                        model_name = each["class_name"]
                        print(f"model_name: {model_name}")  
                        init_objects(model_name, data.get('list_of_objects', []))
                else:      
                    pprint(f"data {data}")          
                    model_name = data['class_name']
                    print(f"model_name: {model_name}")  
                    init_objects(model_name, data.get('list_of_objects', []))
                    
