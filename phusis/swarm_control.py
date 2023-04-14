import openai
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
from phusis.models import *
from noveller.models import *
from .openai_api import *
from .swarm_engines import *

orc_data = {
    "name": "Sam. Our friendly gpt agent ambassador",
    "goals": ["support", "help", "make decisions", "progress the project"],
    "roles": ["user prompting", "constructive criticism", "gpt agent prompting", "combining efforts", "managing", "being the side kick", "offer ideas"],
    "qualifications": ["management", "directing", "project managing", "motivating", "planning"],
    "impersonations": ["Leslie Knope", ""],
    "personality": ["cheerful", "funny", "supportive", "patient", "encouraging", "relaxed"]   
}
orc = {}
structural_engienes = []

all_agent_arrays = [
    structural_engienes
]

def get_all_agents():
    global orc
    all_agents = [orc]
    for agent_array in all_agent_arrays:
        for agent in agent_array:
            all_agents.append(agent)
    return all_agents

def swarm_engage(api):
    global orc
    
    orc.pre_engagement()
    
    for agent in get_all_agents():
        orc.script.current_embedding = api.gpt_embeddings_response(
            orc.script.script_to_text()
        )
        prompt = agent(prompt)
        agent.engage()
        orc.mid_engagement(agent)
    
    orc.post_engagement()

def main():
    api = OpenAi()
    #orchestrator setup
    orc, create = OrchestrationAgent.objects.get_or_create(name=orc_data["name"])
    orc.auto_mode=False
    orc.agent_type='orchestration_agent'
    orc.script.is_master_script=True
    complete_agent_definition(orc, orc_data)
    print("do you want to let the machines run with no user input other than some inital prompting? y/n")
    answer = input("")
    if answer == 'y' : orc.auto_mode=True
    master_script = Script.objects.create(orc)
    pprint(orc)
    
    #get all agent models
    for structural_engiene in StructuralEngine:
        structural_engienes.append(structural_engiene)
    
    #get started 
    master_script._n_print("Hi Let's get started on our story!")    
    master_script._n_print("Do you want me to: \n    1:prompt you for questions or \n    2:just tell me about it?\n      3: point me in the direction of some files?")
    user_choice = master_script._n_user()
    if user_choice == 1:
        user_input=master_script._n_user()
        master_script._n_print("Let's consider our selection of structure agents to help you guide you through your project")
        
        for engine in structural_engienes:
            master_script._n_print(engine.introduction)
        
        master_script._n_print(f"Which of them would you like to work with? (1-{structural_engienes.len()})")
        user_input=master_script._n_user()
        
        chosen_engiens = []
        chosen_engiens.append(structural_engienes.get(user_input))
        master_script._n_print(f"Good choice. Hang on while we warm up: {structural_engienes.get(user_input).get('name')}")
        
        while user_input != "exit!":
            master_script._n_print("You are currently in a prompt loop, getting information about the story you want to work on...")
            u = master_script.loop_return_message_and_prompt()
            if u == "exit!":
                break
            elif u == "":
                swarm_engage(api, )
            else:
                u
        
    elif user_choice == 2:
        
        # user_unprompted_story_data = script._n_user()
        pass
    elif user_choice == 3:
        pass
    
    # user_data = {
        
    # } 

if __name__ == "__main__":
    main()
