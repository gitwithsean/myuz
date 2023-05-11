import os, json
from django.core.management.base import BaseCommand, CommandError
from termcolor import colored
from noveller.noveller_models import Book
from phusis.phusis_utils import load_model_and_return_instance_from, spaced_to_underscore
from phusis.agent_models import AbstractPhusisProject

data_directory =''
app_name = ''   
project_name = ''  
proj_obj = None

class Command(BaseCommand):
    help = 'Load JSON data from files into the app\'s database'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Name of the app containing the project data')
        parser.add_argument('project_name', type=str, help='Quotation enclosed name of the project to init into the db (e.g. "The Nevereding Story"))')

    def handle(self, *args, **options):
        global data_directory
        global app_name
        global project_name
        global proj_obj
        app_name = options['app_name']
        project_name = spaced_to_underscore(options['project_name'])
        data_directory=f"{app_name}/phusis-projects/{app_name}/projects/{project_name}"
        
        if not os.path.exists(f"{data_directory}/init_project/"):
            raise CommandError(f'Data directory not found: {data_directory}/init_project/')
        
        project_json_data = []
                   
        for root, dirs, files in os.walk(f"{data_directory}/init_project/"):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        json_data = json.load(f)
                        for item in json_data:
                            project_json_data.append(item)
        
        json_objects_to_create = []
                        
        for item in project_json_data:
            class_name = item["class_name"]
            list_of_instances = item["list_of_instances"]
            for instance in list_of_instances:
                json_object_to_create = {
                    "class_name": class_name,
                    "properties": instance["properties"]
                }
                json_objects_to_create.append(json_object_to_create)

        for obj_json in json_objects_to_create:
            
            print(colored(f"init_project: loading {app_name} object of class {obj_json['class_name']}, '{obj_json['properties']['name']}'", "yellow"))
            
            obj = load_model_and_return_instance_from(obj_json, app_name)

            if isinstance(obj, Book) and spaced_to_underscore(obj.name).lower() == project_name:
                print(colored(f"init_project: found project {obj.name}", "blue"))
                proj_obj = obj
        
        # print(colored(f"init_project: adding files to project {proj_obj.name} embddings memory", "yellow"))     
        for root, dirs, files in os.walk(f"{data_directory}/files_to_embed/"):
            for file in files:
                file_path = os.path.join(root, file)
                print(colored(f"init_project: adding file {file_path} to project embddings memory", "yellow"))
                proj_obj.add_file_to_memory(file_path)
                print(colored(f"init_project: {file_path} added to project embddings memory", "green"))

