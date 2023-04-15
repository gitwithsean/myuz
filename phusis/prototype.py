from phusis.models import *
from noveller.models import *
import json
from pprint import pprint

#globals
commands = ['exit!', 'go!', 'update!', 'switch_orc!', 'new_agent!']
commands_str = f"\nCOMMANDS: {commands[0]}, {commands[0]}, {commands[0]}\n"
user = {}
orc = {}
story_details = {}
orcs = []
agent_classes = []
agents = []
init_prompts = ['genre(s)', 'character(s)', 'setting', 'target audiences', 'conflicts and resolutions', 'themes', 'style']

def user_init():
    global user
    user = UserAgent()
    
def orcs_init():
    global orc
    orc_names = ""
    with open('phusis/init_data/init_orc_agents.json', 'r') as f: 
        all_orcs_data = json.load(f)
    
    for orc_data in all_orcs_data['orchestration_agents']:
        print(f"Creating orchestration agent: {orc_data['name']}")
        orc_data['__module__'] = 'phusis.models'
        DynamicOrchestrationAgent = type('DynamicOrchestrationAgent', (OrchestrationAgent,), orc_data)
        new_orc = DynamicOrchestrationAgent()
        new_orc.auto_mode = True
        new_orc.init_data=orc_data
        new_orc.script=Script()
        orc_names = new_orc.name + ", " + orc_names
        orcs.append(new_orc)
    
    intro_command = '.intro!'
    user_input = ""
    while not user_input.__contains__(intro_command):
        print(f"Orchestrators available: {orc_names}\n")
        user_input = input(f"\n\nPlease enter the name of the Orchestrater you would like to work with, \nor just hit enter for {orcs[0].name}\nOr if you would like an introduction from an Orchestrator, type their Name{intro_command}")
        orc_name_to_intro = user_input.split(intro_command)[0]
        for orc in orcs:
            if orc_name_to_intro == orc.name:
                print(f"{orc.introduction()}")
    
    while orc == {}:
        print(f"")
        if user_input.strip() == "":
            print(f"No selection made, defaulting to {orcs[0].name}")
            orc_choice = {orcs[0].name}
        else:
            orc_choice = user_input
        print(f"Selecting {orc_choice}")  
        for orc_agent in orcs:          
            if orc_choice == orc_agent.name: 
                orc = orc_agent
                break         
        if orc == {}: 
            user_input = input(f"\n\nSomething went wrong! Perhaps you entered the wrong name? Orchestration Agents available are:\n\n{orc_names}\n\n") 

    print(f"While {orc} wakes up, think about the story you want to work on today.\n\nWhat do you want to tell {orc} to get started? Think about {init_prompts}, etc.\n\n")
    orc.start_engine()

def agents_init():  
    for obj in gc.get_objects():
        if isinstance(obj, AbstractAgent):
            agent_classes.append(obj.__name__)
    agent_classes = list(set(agent_classes))  # Remove duplicates by converting to set and back to list     
    
    with open('phusis/init_data/initial_agents.json', 'r') as f: all_agents_data = json.load(f) 
    
    for agent_data in all_agents_data:
        print(f"Creating {agent_data.agent_type}: {agent_data.name}")
        agent_data['__module__'] = 'phusis.models'
        DynamicAgent = type('DynamicAgent', (AbstractAgent,), agent_data)
        new_agent = DynamicAgent()
        new_agent.auto_mode = True
        new_agent.init_data=agent_data
        new_agent.script=Script()
        agents.add(new_agent)

def user_input_is_command(input):
    global commands
    for command in commands:
        if command == input:
            return True
    return False

def interaction_to_script(sender, prompt, receiver, response):
    print(f"Sender: {sender.name}\n\"{prompt}\"\n\n{receiver.name}\n\"{response}\"")
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
    global story_details
    
    print("Initializing your Orchestration Agents.")
    user_init()
    orcs_init()
    agents_init()
    
    prompt, response = orc.start_engine()
    interaction_to_script(user, prompt, orc, response)

    user_input = input(f"\n\nOK, {orc} is ready for your input: \n\n[or prompt! to receive a list of prompts that will get you started")
    
    if user_input == 'prompt!':
        user_input = ""
        for init_prompt in init_prompts:
            user_input = user_input + {init_prompt} + input(f"tell us about the {init_prompt} of the story") + "\n\n"
        user_input = user_input + input(f"Anything else you want to add?") + "\n\n"
    else:
        while user_input_is_command(user_input) == False:
            user_input = input(f"Enter input. Tell {orc} more about your story...\n\nCOMMANDS: 'go!' 'exit!' 'update!'") 
    
    orc.submit_chat_prompt(user_input, user)
    interaction_to_script(user, prompt, orc, response)
    
    while True:
        iteration = iteration+1
        if user_input == "exit!":
            break
        elif user_input == "go!":
            pass
        elif user_input == "update!":
            orc.script
        else:
            orc.submit_prompt(user_input)

        orc.assess_project(orc.master_script)
        orc.assess_agents()
        orc.next_steps()

        new_agent = orc.create_agents()
        agents.append(new_agent)

        for agent in agents:
            prompt = orc.generate_prompt(agent)
            response = agent.respond(prompt)

            orc.master_script.add_entry(orc, prompt)
            orc.master_script.add_entry(agent, response)

        if not orc.auto_mode and iteration >=5:
            print("Project status update:")
            user_input = input(f"Enter input, tell {orc} more about your story:\n\n{commands_str}")


if __name__ == "__main__":
    main()