import json, os
from django.core.management.base import BaseCommand
from django.apps import apps
import inflect
from phusis.models import *
from pprint import pprint

app_name = ""

def relate_child_to_parent(parent_obj, relationship_name, child_data):
    global app_name
    childrens_names = []
    if isinstance(child_data, str):
        childrens_names.append(child_data)
    elif isinstance(child_data, list):
        childrens_names = child_data
    elif isinstance(child_data, object):
        pass
    elif isinstance(child_data, dict):
        pass        
    
    for child_name in childrens_names:
        relationship_field = getattr(parent_obj, relationship_name)
        child_model = parent_obj.relationship_field.related_model    
        child_obj, created = child_model.objects.get_or_create(name=child_name)
        relationship_field.add(child_obj)

def init_objects(class_name, list_of_objects):
    global app_name
    class_for_objs = apps.get_model(app_name, class_name)
    for obj_data in list_of_objects:
        if class_for_objs.objects.filter(name=obj_data).first():
            new_obj = class_for_objs()
            if 'name' in obj_data:
                new_obj.name = obj_data
                for key in obj_data:
                    if isinstance(obj_data[key], list):
                        for obj_child_data in obj_data[key]:
                            relate_child_to_parent(new_obj, key, obj_child_data)  
                
                new_obj.save()
    pass

class Command(BaseCommand):
    help = "Loads data in {app_name}/init_data/*.json into the database"
    
    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help="The name of the Django app")

    def handle(self, *args, **options):
        global app_name
        app_name = options['app_name']
        self.load_init_data(app_name)
    
    def load_init_data(self, app):
        global app_name
        app_name = app
        for filename in os.listdir(f"{app_name}/init_data/"):
            if not filename.endswith('.json'):
                continue

            with open(os.path.join(f"{app_name}/init_data/", filename), 'r') as f:
                data = json.load(f)
                
                # If one of the top level keys is 'all_class_types'
                if 'all_class_types' in data:
                    for class_type_dict in data['all_class_types']:
                        class_name = class_type_dict['class_name']
                        list_of_objs = class_type_dict['list_of_objects']
                        init_objects(class_name, list_of_objs)
                # If one of the top level keys is 'class_name'     
                elif 'class_name' in data:
                    class_name = data['class_name']
                    list_of_objs = data['list_of_objects']
                    init_objects(class_name, list_of_objs)
                else:
                    print(f"Not currently able to handle this schema:")
                    pprint(data)
                                    