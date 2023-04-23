import os, re
from termcolor import colored
from django.apps import apps
from django.db.models.fields import CharField
from .agent_models import *

PROJECT_ROOT="myuz"
INCOMING_FILES="/files_to_embed/"
OUTGOING_FILES="/files_created/"
LOGS="/logs/"
def get_phusis_project_workspace(project_type, project_name):
    
    if not isinstance(project_type, CharField):
    
        myuz_dir = os.getcwd()
        
        print(colored(f"agent_utils.get_phusis_project_workspace: myuz_dir set to {myuz_dir}", "yellow"))
        
        if PROJECT_ROOT in myuz_dir:
            myuz_dir = myuz_dir[:myuz_dir.index(PROJECT_ROOT) + len(PROJECT_ROOT)]
            
        phusis_project_workspace = f"{myuz_dir}/phusis/phusis_projects/{spaced_to_underscore(project_type)}/{spaced_to_underscore(project_name)}" 
        
        print(colored(f"agent_utils.get_phusis_project_workspace: phusis_project_workspace set to {phusis_project_workspace}", "yellow"))
        
        
        os.makedirs(f"{phusis_project_workspace}{INCOMING_FILES}", exist_ok=True)
        os.makedirs(f"{phusis_project_workspace}{OUTGOING_FILES}", exist_ok=True)
        os.makedirs(f"{phusis_project_workspace}{LOGS}", exist_ok=True)
        
        return phusis_project_workspace 


def camel_case_to_underscore(name):
    print(f"NAME {name}")
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camel_case_to_spaced(name):
    # insert space before every capital letter
    name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
    # convert to lowercase
    name = name.lower()
    return name

def spaced_to_underscore(name):
    return name.replace(" ", "_")

def is_valid_init_json(json_data):
    if not 'class_name' in json_data or not 'properties' in json_data or not 'name' in json_data['properties']:
        return False
    else:
        return True


def add_script_entries_for_each_agent(project, sender, prompt, responder, response):
    project.script_for_project.add_script_entry(sender, prompt, responder, response)    
    sender.script_for_agent.add_script_entry(sender, prompt, responder, response)    
    responder.script_for_agent.add_script_entry(sender, prompt, responder, response)    
    project.save()
    sender.save()
    responder.save()

def get_user_agent_singleton():
    from phusis.agent_models import UserAgentSingleton
    return UserAgentSingleton()

def get_compression_agent_singleton():
    from phusis.agent_models import CompressionAgentSingleton
    return CompressionAgentSingleton()



class PromptBuilderSingleton():
    expose_rest = False
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            # print('Creating PromptBuilder singleton instance')
            cls._instance = super().__new__(cls)
            # Initialize the class attributes here
            cls._instance.prompts_since_reminder = 0
            cls._instance.max_prompts_between_reminders = 5
        return cls._instance
    
    def complete_prompt(self, prompt, prompter):
        prompt = f"The following prompt comes from a {prompter.agent_type}:\n\n--------------------\n\n{prompt}"
        return self.auto_reminder(prompt, prompter)
    
    def auto_reminder(self, prompt, prompter):
        # if self.prompts_since_reminder >= 5:
        #     prompt = f"{prompt} Just Reminding you: {self.to_remind(prompter)}"
        #     self.prompts_since_reminder = 0
        # return f"{prompt}"
        return prompt
                    
    def to_wake_up(self, agent):
        if agent.awareness      =='as_bot':
            s=f"a {agent.agent_type}, part of a swarm of agents, each with a very defined set of attributes."
        elif agent.awareness    =='as_orc':
            s=f"the master orchestrator of a swarm of GPT agents, all working towards a common objective." 
        else:                          
            s="I'm glad to have your expertise on this project."
        
        prompt = f"You are {agent}, {s}. You will use your skills to the BEST of your ability to serve me, the human user, I will tell you our objective soon, but first, about you. {self.to_remind(agent)}"

        return self.auto_reminder(prompt, agent)  
    
    def to_assess(self, assessing_agent, data_to_assess={}):
        prompt = ""
        if 'project' in data_to_assess:
            chats = ""
            swarm_report = ""
            for chat in data_to_assess['script_entries']:
                chats = f"{chats} {chat}\n\n"
            for swarm_report in data_to_assess['swarm_reports']:
                swarm_report = f"{swarm_report} {swarm_report}\n\n"
            project_details = data_to_assess['project'].get_project_details()
            
            prompt = f"Imagine you have within your system, a python script that can take the following paramters and produce an assessment of the project based on the following output schema\n\nParameters:\n\n"
            prompt = prompt + f"RECENT_CHATS: {chats}\n\n"
            prompt = prompt + f"PROJECT_DETAILS: {project_details}\n\n"
            prompt = prompt + f"SWARM_REPORT: {swarm_report}\n\n" 
            prompt = prompt + f"Please prdouce your report in the following schema:\n\n"
            prompt = prompt + f"ASSESSMENT: your_assessment\n\n"
            prompt = prompt + f"PROPOSED_NEXT_STEPS: list_of_proposed_next_steps\n\n"  
            print(colored(f"PromptBuilderSingleton().to_assess: prompt set to {prompt}", "yellow"))
        return self.auto_reminder(prompt, assessing_agent)
    
    def thoughts_concerns_proposed_next_steps(self, agent, agent_to_share_with):
        prompt = f"{agent_to_share_with}, {agent_to_share_with.agent_type} of the swarm you are a member of, has requested for you to report back. They want you to reflect on what you have done so far, and respond in the following format as concisely as possible:\n\nTHOUGHTS:\n\nCONCERNS\n\nWHAT YOU THINK YOUR NEXT STEPS SHOULD BE:\n\n"
        return self.auto_reminder(prompt, agent) 
    
    def to_remind(self, agent):      
        prompt = f"Here is your character description: {agent.to_dict()}"
        
        return self.auto_reminder(prompt, agent)  

    def to_compress(self, prompt, compression_ratio=0.25):
        compression_prompt = f"Compression agent: compress the following text to a ratio <= {compression_ratio} so that another GPT agent will understand the full meaning of the original text. Use abbreviations, symbols, or emojis to assist. It does not need to be human-readable, but it should be easy for another GPT instance to interpret. Here is the text: {prompt}"
        return compression_prompt
        
    def to_ask_opinion_about(self, it, agent):
        prompt = ""

        return self.auto_reminder(prompt, agent) 
    
    def to_ask_next_step(self, agent):
        prompt = ""
        
        return self.auto_reminder(prompt, agent)

