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

def user_input_is_command(input):
    global commands
    for command in commands:
        if command == input:
            return True
    return False

def user_init():
    global user
    user = UserAgentSingleton()
    new_script = Script.objects.create(agent_name=user.name)  
    user.script = new_script    
    
def orcs_init():
    global orc
    orc_names = ""
    with open('phusis/init_data/init_orc_agents.json', 'r') as f: 
        all_orcs_data = json.load(f)
    
    for orc_data in all_orcs_data['orchestration_agents']:
        # print(f"Creating orchestration agent: {orc_data['name']}")
        orc_data['__module__'] = 'phusis.models'
        DynamicOrchestrationAgent = type('DynamicOrchestrationAgent', (OrchestrationAgent,), orc_data)
        new_orc = DynamicOrchestrationAgent()
        new_orc.auto_mode = True
        new_orc.init_data=orc_data
        new_script = Script.objects.create(agent_name=orc_data['name']) 
        new_orc.script = new_script    
        orc_names = new_orc.name + ", " + orc_names
        orcs.append(new_orc)
    
    intro_command = '.intro!'

    while orc == {}: 
        print(f"Orchestrators available: {orc_names}")
        user_input = input(f"\nPlease enter the name of the Orchestrater you would like to work with, \nor just hit enter for {orcs[0].name}\nOr if you would like an introduction from an Orchestrator, type their Name{intro_command}\n")
        while not user_input_is_command(user_input) and user_input.strip() != "":
            if(user_input.__contains__(intro_command)):
                orc_name_to_intro = user_input.split(intro_command)[0]
                for orc in orcs:
                    if orc_name_to_intro == orc.name:
                        print(f"{orc.introduction()}\n")
        
        if user_input.strip() == "":
            print(f"No selection made, defaulting to {orcs[0].name}")
            orc_choice = orcs[0].name
        else:
            orc_choice = user_input
        print(f"Selecting {orc_choice}")  
        for orc_agent in orcs:          
            if orc_choice == orc_agent.name: 
                orc = orc_agent
                break         
        if orc == {}: 
            user_input = input(f"\nSomething went wrong! Perhaps you entered the wrong name? Orchestration Agents available are:\n{orc_names}\n") 

    print(f"While we let {orc} wake up, think about the story you want to work on today.\nWhat do you want to tell {orc} to get started? Think about {init_prompts}, etc.\n")
    orc.start_engine()

def agents_init():  
    with open('phusis/init_data/initial_agents.json', 'r') as f: all_agents_data = json.load(f) 
    # pprint(all_agents_data["all_agents_by_agent_type"])
    for agent_tuple in all_agents_data["all_agents_by_agent_type"]:
        agent_type_class_name = agent_tuple['agent_type_class_name']
        for agent_data in agent_tuple["agents"]:
            # pprint(agent_data)
            # print(f"Creating {agent_type_class_name}: {agent_data['name']}")
            agent_data['__module__'] = 'phusis.models'
            agent_class = globals()[agent_type_class_name]
            new_agent = agent_class(agent_data)
            new_script = Script.objects.create(agent_name=agent_data['name'])  
            new_agent.script = new_script                     
            agents.append(new_agent)


def interaction_to_script(sender, prompt, receiver, response):
    print(f"Sender: {sender.name}\n\"{prompt}\"\n{receiver.name}\n\"{response}\"")
    user.script.add_entry
    if sender.agent_type != 'user' : sender.script.add_entry(sender, prompt, receiver, response)
    if receiver.agent_type != 'user' : receiver.script.add_entry(sender, prompt, receiver, response)
    
def main():
    print("NOVELIER - a phusis application")
    global user
    global orc
    global orcs
    global agent_classes
    global agents
    global project_details
    current_prompt = ""
    print("Select your Orchestration Agents.")
    orcs_init()
    user_init()
    agents_init()
    prompt, response = orc.start_engine()
    interaction_to_script(user, prompt, orc, response)

    user_input = input(f"\nOK, {orc} is ready for your input:\n\n[or prompt! to receive a list of prompts that will get you started]\n\n")
    
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
    
    prompt, response = orc.submit_chat_prompt(user_input, user)
    interaction_to_script(user, prompt, orc, response)
    
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