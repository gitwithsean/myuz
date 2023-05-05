from django.core.management.base import BaseCommand
from phusis.agent_models import *
from noveller.noveller_models import *
from pprint import pprint
from phusis.agent_utils import get_user_agent_singleton

#globals
commands = ['exit!', 'go!', 'update!', 'switch_orc!', 'new_agent!', '.intro!']
commands_str = f"\nCOMMANDS: {commands[0]}, {commands[0]}, {commands[0]}\n"
user = get_user_agent_singleton()
orc = {}
orcs = []
init_prompts = ['genre(s)', 'character(s)', 'setting', 'target audiences', 'conflicts and resolutions', 'themes', 'style']
project = {}

def user_input_is_command(input):
    global commands
    for command in commands:
        if command == input:
            return True
    return False


def user_init():
    global user
    user = get_user_agent_singleton()
   
    
def orcs_init():
    global orc
    print(f"Orchestrators available: ")
    i = 1
    for orchestrator in OrchestrationAgent.objects.all():
        orcs.append(orchestrator)
        print(f"{i}: {orchestrator.name}")
        i = i + 1
    

    user_input = "3"

    # user_input = input("Please enter the number of the orchestrator you would like to lead the project: \n")
    
    i = 1
    for orchestrator in orcs:
        if f"{i}" == user_input: 
            orc = orchestrator 
            print(f"You have selected {orc.name}")
            break
        else: 
            i = i + 1

      
def project_init(): 
    user_init()
    print("Define your Project.")
    project_name = input("Give your project a name\n")
    project_type = input("What type of project is it? Book, script, short story. \nHit enter to set it as Book\n")
    if project_type.strip == '':
        project_type = Book

    new_project = Book()
    new_project.name = project_name
    project_type = new_project.class_display_name
    # new_project.agents_for_project.add(get_user_agent_singleton())
    new_project.save()
    
    add_agents_to_project(new_project)
    new_project.save()
    

def add_agents_to_project(project):

    print("Select your Orchestration Agent.")
    
    orcs_init()
    
    project.orchestrator = orc
        
    print("Waking up agent(s)...\n")
    
    print(f"While we wait, think about the story you want to work on today.\nWhat do you want to tell {orc} to get started? Think about {init_prompts}, etc.\n")

    orc.wake_up()

def retrieve_and_load_project():

    projects_available = Book.objects.all()
    user_selected_project = {}
    print("Projects available to load:")
    i = 1
    for project in projects_available:
        print(f"{i}: {project.name}")
    

    user_input = "1"

    # user_input = input(f"\nPlease enter the number that corresponds to the project you wish to load\n")
    
    i = 1
    for project in projects_available:
        if f"{i}" == user_input: 
            user_selected_project = project 
            # pprint(user_selected_project)
            print(f"You have selected {user_selected_project.name}")
            break
        else: 
            i = i + 1
    
    pprint(user_selected_project)

    if user_selected_project.get_agents_for() == []:
        add_agents_to_project(user_selected_project)
        user_selected_project.save()
    else:
        user = 'y'
        # user = 'n'
        # user = input("Do you want to start again with fresh agents for your project?\n(y/n)\n")
        if user == 'y':   
            if user_selected_project.goals_for_project.exists():
                print(colored(f"deleting memory of {user_selected_project.name}", "yellow"))
                goals = user_selected_project.goals_for_project.all()
                user_selected_project.goals_for_project.clear()
                goals.delete()  
                user_selected_project.save()   
            if user_selected_project.orchestrator != None:
                if orc.chat_logs.exists():
                    print(colored(f"deleting memory for {orc.name}", "yellow"))
                    chat_logs = orc.chat_logs.all()
                    orc.chat_logs.clear()
                    orc.awake = False
                    chat_logs.delete()
                    orc.save()
            add_agents_to_project(user_selected_project)
        else:
            print("loading_data_from_book")
            orc = user_selected_project.orchestrator
    
    return user_selected_project        
    
    
def main():
    print("========================= NOVELIER - a phusis application =========================\n\n")
    global user
    user = get_user_agent_singleton()
    global orc
    global project
    # user_input = input("Welcome. Do you want to start a new project or continue with an existing one? [(n)ew!, (c)ontinue!]\n")
    
    # if user_input == "c" or user_input == 'continue!' or user_input == '(c)ontinue!':
    project = retrieve_and_load_project()
    # else:
    #     project = project_init()

    if not orc.awake:
        print(colored(f"prototype.main() - orc.awake? {orc.awake}", "yellow")) 
        orc.wake_up()
        orc.auto_mode = True
        orc.save()
        
    print(colored(f"prototype.main() - orc.awake: {orc.awake}", "green")) 
            
    iteration = 0
    while True:
        iteration = iteration+1
        print(f"=================ITERATION {iteration}=================")
        orc.routine(project)

if __name__ == "__main__":
    main()
    
class Command(BaseCommand):
    help = 'Run the phusis noveller prototype'
    
    def handle(self, *args, **options):
        main()