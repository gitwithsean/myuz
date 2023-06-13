
import json
from termcolor import colored

class Prompter():
    # Singleton
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    please_respond_with_array = '\nPlease respond with a valid JSON array of comma separated, quotation-enclosed strings, square brackets, all on one line, e.g. ["item one is...", "second item, we think, is...", "item three", ...]'
    
    example_agent_assignments_model = [
            {
                "agent_assigned" : {
                    "agent_already_exists" : True,
                    "agent_type" : "poetics_agent",
                    "agent_name" : "Lyrical Prose",
                },
                "assignment" :{                
                    "assignment_proj_att" : "the project attribute assigned.",
                    "additional_instructions" : "instructions for the agent."
                }
            }
        ]
    example_agent_assignments_model_str = f"{json.dumps(example_agent_assignments_model, separators=(',',':'))}"
    
    
    def auto_reminder(self, prompt, agent):
        # if agent.prompts_since_reminder >= 5:
        #     prompt[content] = f"{prompt} \nAlso, just Reminding you: {self.to_remind(agent)}"
        #     agent.prompts_since_reminder = 0
        # return f"{prompt}"
        # print(colored(f"Prompter.auto_reminder: prompt = {prompt}", "yellow"))
        return prompt
       
                    
    def to_wake_up(self, agent):
        
        prompt = {}
        s = ""
        if agent.awareness == 'as_bot':
            s=f"a GPT {agent.agent_type} and member of a swarm of agents, each with a very defined set of attributes and working towards a common user objective."
        elif agent.awareness == 'as_orc':
            s=f"the master orchestrator and leader of a swarm of GPT agents, each of whom are working towards a common user objective." 
        else:                          
            s="I'm glad to have your expertise on this project."
        
        prompt_content = f"You are '{agent}', {s} You will use your skills to the BEST of your ability to serve me, the human user. {self.to_remind(agent)}."
        
        prompt["content"] = prompt_content
        
        # print(colored(f"Prompt.to_wake_up: prompt set to \n{prompt}", "yellow"))

        return prompt
    
    
    def to_establish_project_goals(self, project, agent):
        prompt = {}
        prompt["example_output_schema"] = self.please_respond_with_array
        prompt_content = f"{project.project_brief()}\n"
        prompt_content += f"# Project Attributes:\nThese are all the attributes available for a project like this:\n{project.project_attributes_to_md()}\n\n"
        prompt_content += f"Using the informtation provided, please define a number of High Level Goals, in the order they need to be achieved, to complete this project.\n"
        prompt_content += self.please_respond_with_array
        prompt["content"] = prompt_content
        return self.auto_reminder(prompt, agent)
    
    
    def to_set_steps_for_project_goal(self, goal, project, agent):
        prompt = {}
        prompt["example_output_schema"] = self.please_respond_with_array
        prompt_content = "You recently set these goals for the project we are working on:\n"
        prompt_content += f"{project.goals_for_project_to_str()}\n"
        prompt_content += f"I would like for you now to split the goal '{goal}' into an ordered list of steps that an agent in the swarm could be directed to take.\n"
        prompt_content += self.please_respond_with_array 
        prompt["content"] = prompt_content
        return self.auto_reminder(prompt, agent)
        
    
    def to_assign_project_attributes_to_step(self, step, goal, project, agent):
        prompt = {}
        prompt["example_output_schema"] = self.please_respond_with_array
        prompt_content = f"You recently listed a number of steps to achieve this goal for a project we are working on.\nGoal: {goal.name}\n"
        prompt_content += f"The project iteslf has these attribute types, each project attribute may have multiple instances (e.g. multiple chapters for a Chapter attribute)\n\n{project.project_attributes_to_md()}\n"
        prompt_content += f"Please consider the step, '{step.name}', and list 0, 1 or 2 project attributes you believe should be related to that step. If you believe there is a project attribute missing from the list above, feel free to suggest one by adding it to the list.\n"
        prompt_content += self.please_respond_with_array
        prompt["content"] = prompt_content
        return self.auto_reminder(prompt, agent)
    
    
    def to_create_agent_assignments_for_step(self, step, agent):
        prompt = {}
        prompt["example_output_schema"] = f"{self.example_agent_assignments_model_str}"
        prompt_content = "You recently assigned project attributes to a step in a project we are working on (though some steps might be assigned to no attribute).\n"
        prompt_content += f"Step: {step.name}\n"
        prompt_content += f"Project Attributes:\n{step.to_dict()['related_project_attributes']}\n\n"
        prompt_content += f"It is now time to assign a GPT agent of the swarm to work on this step (and/or it's attributes).\n"
        prompt_content += f"Here is a list of all the agent types and instances of those types available to the swarm\n"
        prompt_content += f"{self.to_learn_about_agent_types()['content']}"
        prompt_content += f"\nPlease respond ONLY with valid JSON in the same schema as the example below, to create one or more agent assignments for this step. All fields are required unless otherwise stated. If you believe there is an agent you need that isn't listed, feel free to create one.\n"
        prompt_content += self.example_agent_assignments_model_str
        prompt["content"] = prompt_content
        # print(colored(f"Prompt.to_create_agent_assignments_for_step: prompt['example_output_schema'] set to \n{prompt['example_output_schema']}", "yellow"))
        
        return self.auto_reminder(prompt, agent)
    
          
    def to_learn_about_agent_types(self):
        from .agent_models import AbstractAgent
        
        prompt = {}
        
        list_of_agent_types = AbstractAgent.__subclasses__()
        
        prompt_content = "# Swarm Agents\n\n"
        
        for agent_type in reversed(list_of_agent_types):
            
            if "UserAgentSingleton" in agent_type.__name__ or "Abstract" in agent_type.__name__  or "OrchestrationAgent" in agent_type.__name__ or 'Concrete' in agent_type.__name__ or 'Dynamic' in agent_type.__name__:
                continue   
            else:
                # print(colored(f"Prompt.to_learn_about_agent_types: agent_type is {agent_type}", "yellow"))
                prompt_content += f"\n## {agent_type.__name__}\n"
                prompt_content += f"### Description:\n{agent_type.type_description}\n"
                prompt_content += f"### Instances Available:\n"
                for agent_instance in agent_type.objects.all():
                    prompt_content += f"* {agent_instance.name}\n"

        prompt["content"] = prompt_content
        return prompt
    
    def to_assign_agent_to_goal(self, goal):
        from .agent_models import AbstractAgent
        
        list_of_agent_types = AbstractAgent.__subclasses__()
    
        prompt = {}
        prompt_content = "# GPT Agent Types\n\n"
        
        for agent_type in list_of_agent_types:
            if "UserAgentSingleton" in agent_type.__name__ or "Abstract" in agent_type.__name__  or "OrchestrationAgent" in agent_type.__name__:
                continue
            else:
                prompt_content += f"\n## {agent_type.__name__}\n"
                for agent_instance in agent_type.objects.all():
                    agent_to_dict, agent_to_string = agent_instance.to_dict_and_string()
                    prompt_content += agent_to_string
    
        
        prompt_content += f"Please assign a GPT agent, or write a prompt to initialize an agent you wish to add to the following goal: {goal}\n"
        prompt_content += "Leave your response only in this JSON format {goal_for_agent: goal, agent_chosen: {agent_type: agent_type, agent_name: agent_name, new_agent_prompt: the prompt you want to give the new agent if you want to create one}}\n"
        
        prompt["content"] = prompt_content
        return prompt
    
        
    def to_remind(self, agent):
        dict, str = agent.to_dict_and_string()    
        prompt = {}  
        prompt_content = f" These are your attributes: \n{str}"
       
        # print(colored(f"PromptBuilderSingleton().to_remind: prompt set to {prompt}", "yellow"))
        
        return self.auto_reminder(prompt, agent)  
