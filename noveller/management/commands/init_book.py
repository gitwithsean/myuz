import os, json
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from pprint import pprint
from termcolor import colored
from noveller.noveller_models import load_noveller_model_and_return_instance_from

data_directory =''
app_name = ''     
        
class Command(BaseCommand):
    help = 'Load JSON data from files into the app\'s database'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Name of the app containing the book data')

    def handle(self, *args, **options):
        global data_directory
        global app_name
        app_name = options['app_name']
        data_directory=f"{app_name}/project_data/"
        
        if not os.path.exists(data_directory):
            raise CommandError(f'Data directory not found: {data_directory}')

        # print(colored(f"app_name is {app_name}", "green"))
        
        book_json_data = []
                   
        for root, dirs, files in os.walk(data_directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        json_data = json.load(f)
                        for item in json_data:
                            # print(item)
                            book_json_data.append(item)
        
        # print(book_json_data)
        
        json_objects_to_create = []
                        
        for item in book_json_data:
            # print(item)
            class_name = item["class_name"]
            list_of_instances = item["list_of_instances"]
            # print(f"class_name: {class_name}")
            # print(f"list_of_instances: {list_of_instances}\n\n")
            for instance in list_of_instances:
                json_object_to_create = {
                    "class_name": class_name,
                    "properties": instance["properties"]
                }
                # print(colored(f"creating {json_object_to_create}", "yellow"))
                json_objects_to_create.append(json_object_to_create)

        for obj_json in json_objects_to_create:
            
            # pprint(obj_json)
            print(colored(f"init_book: loading {obj_json['class_name']} {obj_json['properties']['name']}", "yellow"))
            
            load_noveller_model_and_return_instance_from(obj_json)
