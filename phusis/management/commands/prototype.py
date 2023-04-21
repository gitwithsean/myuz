from django.core.management.base import BaseCommand, CommandError

from phusis.models import *
from noveller.models import *
import json
from pprint import pprint

#globals
commands = ['exit!', 'go!', 'update!', 'switch_orc!', 'new_agent!', '.intro!']
commands_str = f"\nCOMMANDS: {commands[0]}, {commands[0]}, {commands[0]}\n"
agent_types = ['structural_agents']
user = {}
orc = {}
project_details = []
orcs = []
agent_classes = []
agents = []
init_prompts = ['genre(s)', 'character(s)', 'setting', 'target audiences', 'conflicts and resolutions', 'themes', 'style']
user_selected_agents = []
current_project = {}

def user_input_is_command(input):
    global commands
    for command in commands:
        if command == input:
            return True
    return False


def user_init():
    global user
    user = UserAgentSingleton()  
   
    
def orcs_init():
    global orc
    orc_names = ""
    
    for orchestrator in OrchestrationAgent.objects.all():
        orc_names = orchestrator.name + ", " + orc_names
        orcs.append(orchestrator)
    
    intro_command = '.intro!'

    while orc == {}: 
        print(f"Orchestrators available: {orc_names}")
        chosen_orc_name = input(f"\nPlease enter the name of the Orchestrater you would like to work with, \nor just hit enter for {orcs[0].name}\nOr if you would like an introduction from an Orchestrator, type their Name{intro_command}\n")
        
        while not user_input_is_command(chosen_orc_name) and chosen_orc_name.strip() != "" and orc == {}:
            if(chosen_orc_name.__contains__(intro_command)):
                orc_name_to_intro = chosen_orc_name.split(intro_command)[0]
                for orc in orcs:
                    if orc_name_to_intro == orc.name:
                        print(f"{orc.introduce_yourself()}\n")
        
            if chosen_orc_name.strip() == " ":
                print(f"No selection made, defaulting to {orcs[0].name}")
                orc_choice = orcs[0].name
            else:
                orc_choice = chosen_orc_name
            
            print(f"Selecting {orc_choice}")  
            
            for orc_agent in orcs:          
                if orc_choice == orc_agent.name: 
                    orc = orc_agent
                    break         
            if orc == {}: 
                user_input = input(f"\nSomething went wrong! Perhaps you entered the wrong name? Orchestration Agents available are:\n{orc_names}\n") 


def agents_init():
    global user_selected_agents
    
    all_agent_classes = AbstractAgent.__subclasses__()
    agent_classes_with_their_instances = []
    
    for agent_class in all_agent_classes:
        instances_for_agent_class = agent_class.get_instances()
        if instances_for_agent_class:
            class_with_instances = {"agent_class": f"{agent_class.__name__()}", "agent_instances": [instances_for_agent_class]}
            agent_classes_with_their_instances.append(class_with_instances)
        else:
            print(colored(f"Message for dev/admin: No instances yet loaded for {agent_class}", "yellow"))    
    
    print("You will now be asked to select the other agents you want to work on this project, there will be these types of agents:")
    for item in agent_classes_with_their_instances:
         print(item['agent_class'].__name__())
         
    for agent_class_with_instances in agent_classes_with_their_instances:
        print(f"First, the {agent_class_with_instances['agent_class'].__name__()} type")
        i = 1
        for agent in agent_class_with_instances:
            print(f"{i} {agent}")
            i = i + 1
    
        user_input = input(f"\nPlease enter the number that corresponds to the agent you wish to assign to this project\n")
        i = 1
        for agent in agent_class_with_instances:
            if i == user_input: 
                user_selected_agent = agent 
                break
            else: 
                i = i + 1
        
        user_selected_agents.append(user_selected_agent)
                
            
def project_init(): 
    user_init()
    print("Define your Project.")
    project_name = input("Give your project a name")
    project_type = input("What type of project is it? Book, script, short story. Hit enter to set it as Book")
    if project_type.strip == '':
        project_type = Book

    new_project = Book()
    new_project.name = project_name
    project_type = new_project.class_display_name
    new_project.agents_for_project(user)
    new_project.save()
    
    add_agents_to_project(new_project)
    new_project.save()
    

def add_agents_to_project(project):

    project.save

    pprint(project)

    print("Select your Agents.")
    orcs_init()
    # orc.save()
    
    
    # from django.db import connection
    relationship = AgentBookRelationship(agent=orc, book=project)
    # try:
    relationship.save()
    # except:
    #     print(connection.queries[-1])
    
    # relationship = AgentBookRelationship(agent=orc, book=project)
    # relationship.save()
    
    # project.agents_for_project.add(orc)
    # project.save()
    
    agents_init()
    for agent in user_selected_agents:
        relationship = AgentBookRelationship(agent=agent, book=project)
        relationship.save()
        # project.add_agent_for_book(agent)
    
    project.save()
    
    print("Waking up agents...\n")
    
    print(f"While we wait, think about the story you want to work on today.\nWhat do you want to tell {orc} to get started? Think about {init_prompts}, etc.\n")

    prompt, response = orc.wake_up()
    interaction_to_script(user, prompt, orc, response)

    for agent in user_selected_agents:
        prompt, response = agent.wake_up()
        interaction_to_script(user, prompt, agent, response)

    user_input = input(f"\nOK, {orc} is ready for your input...")
                       
                    #    \n\n[or type prompt! to receive a list of prompts that will get you started]\n\n")
            
    prompt, response = orc.submit_chat_prompt(user_input, user)
    interaction_to_script(user, prompt, orc, response)
    
    
    # current_prompt = user_input
    
    # if user_input == 'prompt!':
    #     user_input = ""
    #     for init_prompt in init_prompts:
    #         user_input = user_input + {init_prompt} + input(f"tell us about the {init_prompt} of the story") + "\n"
    #         user_input = user_input + input(f"Anything else you want to add?") + "\n"\
        
    #     project_details.append(user_input.__str__())
    # else:
    #     while user_input_is_command(user_input) == False:
    #         project_details.append(user_input.__str__())
    #         user_input = input(f"Enter input. Tell {orc} more about your story...\nCOMMANDS: 'go!' 'exit!' 'update!'") 
        #         if not user_input_is_command: project_details.append(user_input.__str__())
        
        # user_input


def retrieve_and_load_project():
    projects_available = Book.objects.all()
    user_selected_project = {}
    print("Projects available to load:")
    i = 1
    for project in projects_available:
        print(f"{i}: {project.name}")
        
    user_input = input(f"\nPlease enter the number that corresponds to the agent you wish to assign to this project\n")
    i = 1
    for project in projects_available:
        if f"{i}" == user_input: 
            user_selected_project = project 
            # pprint(user_selected_project)
            print(f"You have selected {user_selected_project.name}")

        else: 
            i = i + 1
    
    change_agents = input("Do you want to change or add the agents in your project?\n(y/n)\n")
    
    if change_agents == 'y':
        add_agents_to_project(user_selected_project)
    else:
        for agent in project.agents_for_project:
            if agent.type == "orchestration_agent": orc = agent
            else: user_selected_agents.append(agent)
    
    return user_selected_project        


def interaction_to_script(sender, prompt, receiver, response):
    print(f"Sender: {sender.name}\n\"{prompt}\"\n{receiver.name}\n\"{response}\"")
    user.script.add_entry
    if sender.agent_type != 'user' : sender.script.add_entry(sender, prompt, receiver, response)
    if receiver.agent_type != 'user' : receiver.script.add_entry(sender, prompt, receiver, response)
  
    
def main():
    print("========================= NOVELIER - a phusis application =========================\n\n")
    global user
    global orc
    global orcs
    global agent_classes
    global agents
    global project_details
    global user_selected_agents
    global current_project
    current_prompt = ""
    user_input = input("Welcome. Do you want to start a new project or continue with an existing one? [(n)ew!, (c)ontinue!]\n")
    
    if user_input == "c" or user_input == 'continue!' or user_input == '(c)ontinue!':
        current_project = retrieve_and_load_project()
    else:
        current_project = project_init()
        
    
    iteration = 0
    while True:
        iteration = iteration+1
        print(f"=================ITERATION {iteration}=================")
        # if user_input == "exit!":
        #     break
        # elif user_input == "go!":
        #     pass
        # elif user_input == "update!":
        #     orc.script
        # else:
        #     orc.submit_prompt(user_input)

        prompt, response = orc.assess_project(project_details)
        interaction_to_script(user, prompt, orc, response)
        prompt, response = orc.amend_project()
        interaction_to_script(user, prompt, orc, response)
        orc.continue_project()

        # new_agent = orc.create_agents()
        # agents.append(new_agent)

        # for agent in agents:
        #     prompt = orc.generate_prompt(agent)
        #     response = agent.respond(prompt)

        #     orc.master_script.add_entry(orc, prompt)
        #     orc.master_script.add_entry(agent, response)

        if not orc.auto_mode:
            print("Project status update:")
            user_input = input(f"Enter input, tell {orc} more about your story:\n{commands_str}")
            project_details.append(user_input.__str__)


if __name__ == "__main__":
    main()
    
class Command(BaseCommand):
    
    def handle(self, *args, **options):
        main()