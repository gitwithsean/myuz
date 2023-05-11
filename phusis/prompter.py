
import json
from django import apps
from termcolor import colored
from .phusis_utils import model_has_content_and_content

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
                "is_new" : False,
                "agent_type" : "poetics_agent",
                "agent_name" : "Lyrical Prose",
            },
            "assignment" :{                
                "assignment_proj_att" : "Optional, the project attribute assigned.",
                "assignment_str" : "Optional, but required if no project attribute assigned, enter your instructions for the agent here."

            }
        }
    ]
    example_agent_assignments_model_str = f"agent_assignments:{json.dumps(example_agent_assignments_model, separators=(',',':'))}"
    
    
    def auto_reminder(self, prompt, agent):
        # if agent.prompts_since_reminder >= 5:
        #     prompt = f"{prompt} \nAlso, just Reminding you: {self.to_remind(agent)}"
        #     agent.prompts_since_reminder = 0
        # return f"{prompt}"
        return prompt
       
                    
    def to_wake_up(self, agent):
        s = ""
        if agent.awareness      =='as_bot':
            s=f"a GPT {agent.agent_type} and member of a swarm of agents, each with a very defined set of attributes and working towards a common user objective."
        elif agent.awareness    =='as_orc':
            s=f"the master orchestrator and leader of a swarm of GPT agents, each of whom are working towards a common user objective." 
        else:                          
            s="I'm glad to have your expertise on this project."
        
        prompt = f"You are '{agent}', {s} You will use your skills to the BEST of your ability to serve me, the human user. {self.to_remind(agent)}."

        # print(colored(f"Prompt.to_wake_up: prompt set to \n{prompt}", "yellow"))

        return prompt
    
    
    def to_establish_project_goals(self, project, agent):
        prompt = f"{project.project_brief()}\n"
        prompt += f"# Project Attributes:\nThese are all the attributes available for a project like this:\n{project.project_attributes_to_md()}\n\n"
        prompt += f"Using the informtation provided, please define a number of High Level Goals, in the order they need to be achieved, to complete this project.\n"
        prompt += self.please_respond_with_array
        return self.auto_reminder(prompt, agent)
    
    
    def to_set_steps_for_project_goal(self, goal, project, agent):
        prompt = "You recently set these goals for the project we are working on:\n"
        prompt += f"{project.goals_for_project_to_str()}\n"
        prompt += f"I would like for you now to split the goal '{goal}' into an ordered list of steps that an agent in the swarm could be directed to take.\n"
        prompt += self.please_respond_with_array 
        return self.auto_reminder(prompt, agent)
        
    
    def to_assign_project_attributes_to_step(self, step, goal, project, agent):
        prompt = f"You recently lited these steps to achieve a goal for a project we are working on.\nGoal: {goal.name}\nSteps:\n"
        prompt += f"{goal.steps_for_goal_to_str()}"
        prompt += f"The project iteslf has these attribute types, each project attribute may have multiple instances (e.g. multiple chapters for a Chapter attribute)\n\n{project.project_attributes_to_md()}\n"
        prompt += f"Please consider the step, '{step.name}', and list 0, 1 or 2 project attributes you believe should be related to that step. If you believe there is a project attribute missing from the list above, feel free to create one.\n"
        prompt += self.please_respond_with_array
        return self.auto_reminder(prompt, agent)
    
    
    def to_create_agent_assignments_for_step(self, step, project, agent):
        prompt = "You recently assigned project attributes to a step in a project we are working on (though some steps might be assigned to no attribute).\n"
        prompt += f"Step: {step.name}\n"
        prompt += f"Project Attributes:\n{step.project_attributes}\n\n"
        prompt += f"It is now time to assign a GPT agent of the swarm to work on this step (and/or it's attributes).\n"
        prompt += f"Please create one or more agent assignments for this step using the JSON representation below. If you believe there is an agent you need that isn't listed, feel free to create one.\n"
        prompt += self.example_agent_assignments_model_str
        return self.auto_reminder(prompt, agent)
    
          
    def to_learn_about_agent_types(self, purpose):
        from .agent_models import AbstractAgent
        
        list_of_agent_types = AbstractAgent.__subclasses__()
        
        prompt = "# GPT Agent Types\n\n"
        
        for agent_type in list_of_agent_types:
            prompt += f"## {agent_type.__name__}\n"
            prompt += f"{agent_type.__description__}\n\n"

        prompt += f"Which of these agent types do you want to assign to the following purpose?\n\n{purpose}"
    
    
    def to_assign_agent_to_goal(self, goal):
        from .agent_models import AbstractAgent
        
        list_of_agent_types = AbstractAgent.__subclasses__()
    
        prompt = "# GPT Agent Types\n\n"
        
        for agent_type in list_of_agent_types:
            if "UserAgentSingleton" in agent_type.__name__ or "Abstract" in agent_type.__name__  or "OrchestrationAgent" in agent_type.__name__:
                continue
            else:
                prompt += f"\n## {agent_type.__name__}\n"
                for agent_instance in agent_type.objects.all():
                    agent_to_dict, agent_to_string = agent_instance.to_dict_and_string()
                    prompt += agent_to_string
    
        
        prompt += f"Please assign a GPT agent, or write a prompt to initialize an agent you wish to add to the following goal: {goal}\n"
        prompt += "Leave your response only in this JSON format {goal_for_agent: goal, agent_chosen: {agent_type: agent_type, agent_name: agent_name, new_agent_prompt: the prompt you want to give the new agent if you wnat to create one}}\n"
        
        return prompt
    
        
    def to_remind(self, agent):
        dict, str = agent.to_dict_and_string()      
        prompt = f" These are your attributes: \n{str}"
        
        # print(colored(f"PromptBuilderSingleton().to_remind: prompt set to {prompt}", "yellow"))
        
        return self.auto_reminder(prompt, agent)  
