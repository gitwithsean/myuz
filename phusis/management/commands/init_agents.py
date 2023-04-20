import os, json
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from pprint import pprint
from phusis.models import load_agent_capabilities_from, load_agent_model_and_return_instance_from
from termcolor import colored

def load_capabilities():
    init_capabilities_json_dir = "phusis/init_data/init_agent_capability.json"

    with open(init_capabilities_json_dir, 'r') as file:
        list_of_capabilities_data = json.load(file)
        
        # pprint(list_of_capabilities_data)
    for data in list_of_capabilities_data:    
        print(colored(f"init_agents.load_capabilities(): loading capability {data['properties']['name']}", "yellow"))
        load_agent_capabilities_from(data)


class Command(BaseCommand):
    help = 'Load JSON data from files into the app\'s database'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Name of the app containing the models')

    def handle(self, *args, **options):
        app_name = options['app_name']
        data_directory=f"{app_name}/secret_sauce/phusis-secret-sauce/agent_data"
        
        if not os.path.exists(data_directory):
            raise CommandError(f'Data directory not found: {data_directory}')

        print(colored(f"app_name is {app_name}", "green"))

        if app_name == "phusis":
            print(colored(f"init_agents {app_name}: Loading Agent Capabilities", "green"))
            load_capabilities()
            
        for file_name in os.listdir(data_directory):
            if file_name.endswith('.json'):

                with open(os.path.join(data_directory, file_name), 'r') as file:
                    data = json.load(file)

                for item in data:
                    print(colored(f"Loading Agent {item['class_name'] }{item['properties']['name']} into db", "yellow"))
                    load_agent_model_and_return_instance_from(item)

