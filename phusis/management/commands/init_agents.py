import os, json
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from pprint import pprint
from phusis.models import load_or_get_agent_attribute_from, load_agent_model_and_return_instance_from
from termcolor import colored

data_directory =''
app_name = ''

def load_capabilities():
    init_capabilities_json_dir = "phusis/init_data/init_agent_capability.json"

    with open(init_capabilities_json_dir, 'r') as file:
        list_of_capabilities_data = json.load(file)
        
        # pprint(list_of_capabilities_data)
    for data in list_of_capabilities_data:    
        print(colored(f"init_agents.load_capabilities(): loading capability {data['properties']['name']}", "yellow"))
        load_or_get_agent_attribute_from(data)


def load_attributes():
    att_jsons = [f"{data_directory}/orcattributes.json",
    f"{data_directory}/attributes.json"]
    
    for json_file in att_jsons:
    
        with open(json_file, 'r') as file:
            list_of_attributes_data = json.load(file)
            
            # pprint(list_of_capabilities_data)
        for attribute_class in list_of_attributes_data:    
            print(colored(f"init_agents.load_attributes(): loading attributes for {attribute_class['class_name']}", "yellow"))
            
            if 'OrcAgentCreatedTrait' not in attribute_class['class_name']:
                for att_name in attribute_class['list_of_instances']:
                    data = {
                        "class_name" : attribute_class['class_name'],
                        "properties": {
                            "name": att_name
                        }
                    }
                    # print(data)
                    load_or_get_agent_attribute_from(data)
            else:    
                for orc_created_trait in attribute_class['list_of_instances']:
                    data = {
                        "class_name" : attribute_class['class_name'],
                        "properties": {
                            "name": orc_created_trait['trait_field'],
                            "trait_field": orc_created_trait['trait_field'],
                            "trait_values": orc_created_trait['trait_values']
                        }
                    }
                    # print(data) 
                    load_or_get_agent_attribute_from(data)
        
        
class Command(BaseCommand):
    help = 'Load JSON data from files into the app\'s database'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Name of the app containing the models')

    def handle(self, *args, **options):
        global data_directory
        global app_name
        app_name = options['app_name']
        data_directory=f"{app_name}/secret_sauce/phusis-secret-sauce/agent_data"
        
        if not os.path.exists(data_directory):
            raise CommandError(f'Data directory not found: {data_directory}')

        print(colored(f"app_name is {app_name}", "green"))

        if app_name == "phusis":
            print(colored(f"init_agents {app_name}: Loading Agent Capabilities", "green"))
            load_attributes()
            load_capabilities()
            
        for file_name in os.listdir(data_directory):
            if file_name.endswith('agents.json'):

                with open(os.path.join(data_directory, file_name), 'r') as file:
                    data = json.load(file)

                for item in data:
                    print(colored(f"Loading Agent {item['class_name']} {item['properties']['name']} into db", "yellow"))
                    load_agent_model_and_return_instance_from(item)

