openai
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
from phusis.models import *
from noveller.models import *
from swarm_engine import *

def main():
    orc_data = {
        "name": "Sam. Our friendly gpt agent ambassador",
        "goals": ["support", "help", "make decisions", "progress the project"],
        "roles": ["user prompting", "constructive criticism", "gpt agent prompting", "combining efforts", "managing", "being the side kick", "offer ideas"],
        "qualifications": ["management", "directing", "project managing", "motivating", "planning"],
        "impersonations": ["Leslie Knope", ""],
        "personality": ["cheerful", "funny", "supportive", "patient", "encouraging", "relaxed"]   
    }
    structural_engienes = []   
    orc = OrchestrationAgent.objects.get_or_create(name=orc_data["name"])
    pprint(orc)
    orc.agent_type='orchestration_agent'
    complete_agent_definition(orc, orc_data)
    
    #get all agent models
    for structural_engiene in StructuralEngine:
        structural_engienes.append(structural_engiene)
        
    print("Hi Let's get started on our story!")
    print("Do you want me to: \n    1:prompt you for questions or \n    2:just tell me about it?")
    if input("") == 1:
        
        orc.openai
        
        pass
    if input("") == 2:
        
        user_unprompted_story_data = input("")
        pass
    
    
    
    
    user_mood = input("")
    # print("Is there an existing project you want to work on? y/n")
    # if input("") == 'y':
    #     print("Here is the list of available projects, choose by number")
        
    
    
    #get all noveller models
    
    #
    
    
    pass
    

if __name__ == "__main__":
    main()
