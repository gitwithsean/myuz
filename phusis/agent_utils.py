import re, json
from termcolor import colored
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist


def model_has_content_and_content(model):
    try:
        content = model.objects.all()
        if content.exists():
            return True, content
        else:
            return False, None
    except ObjectDoesNotExist:
        return False, None


def camel_case_to_underscore(name):
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


def memorize_chat(prompt, response, responder):
    from phusis.agent_memory import ProjectMemory
    new_chat_log = responder.add_to_chat_logs(prompt, response)
    ProjectMemory().add_chat_log_db_instance_to_pinecone_memory(new_chat_log)


def memorize_chat(chat_log):
    from phusis.agent_memory import ProjectMemory
    # print(colored(f"agent_uitls.memorize_chat(): {chat_log}", "yellow"))
    ProjectMemory().add_chat_log_db_instance_to_pinecone_memory(chat_log)    


def get_embeddings_for(text):
    from phusis.apis import OpenAiAPI
    return OpenAiAPI().get_embeddings_for(text)


def get_user_agent_singleton():
    from phusis.agent_models import UserAgentSingleton
    return UserAgentSingleton()


def load_model_and_return_instance_from(json_data, app_name):
    """
    With dict json_data and app_name and parms either create or find an instance based on the provided JSON data in app_name and return it.
    
    Args:
        json_data (dict): A dictionary containing the JSON data for the model.
        app_name (str): The name of the app to search for or create the model in.
    
    Returns:
        object: An instance of the model created or updated based on the JSON data.
    """
    
    new_project_obj = {}
    expected_json = {
        "class_name": "ModelClassName",
        "properties": {
            "name": "Instance Name"
        }
    }
 
    if is_valid_init_json(json_data):
        try:
            model_class = apps.get_model(app_name, f"{json_data['class_name']}")
        except LookupError:
            print(colored(f"agent_utils.create_project_model_from_instance: class_name {json_data['class_name']} not found in globals()", "red"))

        # print(colored(f"agent_utils.create_project_model_from_instance: model_class {model_class}. json_data['properties']['name'] {json_data['properties']['name']}", "green"))

        new_project_obj, created = model_class.objects.update_or_create(name=json_data['properties']['name'])

        new_project_obj.set_data(json_data['properties'])
        new_project_obj.save()
        s = f"found and updated with:\n{json_data['properties']}"
        if created: s = "created"
        # print(colored(f"agent_utils.create_project_model_from_instance: {new_project_obj.name} {s}", "green"))
        
    else:
        print(colored(f"agent_utils.create_project_model_from_instance: JSON data for model not valid, minimum expected schema below","red"))
        print(colored(f"Data received: {json_data}", "red"))
        print(colored(f"Minimum expected: {expected_json}", "yellow"))

    return new_project_obj


def find_and_update_or_create_attribute_by(attr_name, model_class):
    """
    Args:
        attr_name (str): The name of the attribute to find or create.
        model_class (class): The model class to search for the attribute in.

    Returns:
        tuple: A tuple containing the attribute class and the attribute instance.
    """

    # print(colored(f"agent_utils.find_and_update_or_create_attribute_by(): attr_name: {attr_name}\nmodel_class : {model_class}", "yellow"))
    
    # Check if the attribute exists in the model class
    if hasattr(model_class, attr_name):
        return model_class, getattr(model_class, attr_name)

    # print(colored(f"model class : {model_class}", "yellow"))

    # Check if the attribute exists in any related models
    for related_object in model_class._meta.related_objects:
        related_model_class = related_object.related_model

        if hasattr(related_model_class, attr_name):
            # Create an instance of the related model to return
            instance = related_model_class.objects.get(**{related_object.field.name: model_class})
            return related_model_class, instance
        else:
            #If the Attribute wasn't found, create it 
            new_attribute, created = model_class.objects.update_or_create(name=attr_name)
            return related_model_class, new_attribute


class Prompt():
    expose_rest = False
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    please_respond_with_array = '\nPlease respond with an iterable array of comma separated, quotation-enclosed strings, no new lines, e.g. ["item one is...", "second item, we think, is...", "item three", ...]'
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
            s=f"a GPT {agent.agent_type} and member of a swarm of agents, each with a very defined set of attributes,  working towards a common user objective."
        elif agent.awareness    =='as_orc':
            s=f"the master orchestrator and leader of a swarm of GPT agents, all working towards a common user objective." 
        else:                          
            s="I'm glad to have your expertise on this project."
        
        prompt = f"You are '{agent}', {s} You will use your skills to the BEST of your ability to serve me, the human user. These are your attributes:\n {self.to_remind(agent)}."

        # print(colored(f"Prompt.to_wake_up: prompt set to \n{prompt}", "yellow"))

        return prompt
    
    
    def to_establish_project_goals(self, project, agent):
        prompt = f"{project.project_brief()}\n"
        prompt += f"### Project Attributes:\n{project.project_attributes_to_md()}\n\n"
        prompt += f"Using the informtation provided, please define a number of High Level Goals, in the order they need to be achieved, to complete this project.\n"
        prompt += self.please_respond_with_array
        return self.auto_reminder(prompt, agent)
    
    
    def to_set_steps_for_project_goal(self, goal, project, agent):
        prompt = "You recently set these goals for the project we are working on:\n"
        prompt += f"{project.goals_for_project}\n"
        prompt += f"I would like for you now to split the goal {goal} into an ordered list of steps that an agent in the swarm could be directed to take.\n"
        prompt += self.please_respond_with_array 
        return self.auto_reminder(prompt, agent)
        
    
    def to_assign_project_attributes_to_step(self, step, goal, project, agent):
        prompt = f"You recently lited these steps to achieve a goal for a project we are working on.\nGoal: {goal.name}\n Steps:\n"
        prompt += f"{goal.steps}\n"
        prompt += f"The project iteslf has these attribute types, each project attribute may have multiple instances (e.g. multiple chapters for a Chapter attribute)\n\n{project.project_attributes_to_md()}\n"
        prompt += f"Please consider the step, {step.name}, and list 0, 1 or 2 project attributes you believe should be related to that step. If you believe there is a project attribute missing from the list above, feel free to create one.\n"
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
    
    
    def to_assess_project_state(self, project, agent):
        models_dict, book_attributes_str = project.list_project_attributes()
        prompt = "# Project Current State:\n\n"
        for model_name, fields in models_dict.items():
            model = apps.get_model(project.from_app, model_name)
            has_content, content = model_has_content_and_content(model)

            prompt += f"## Model: {model_name}\n"
            prompt += f"- Has Content: {has_content}\n"
            if has_content:
                prompt += "### Content:\n"
                for obj in content:
                    prompt += f"  - {obj}\n"

            prompt += "### Fields:\n"
            for field in fields:
                prompt += f"  - {field}\n"

            prompt += "\n"
            
        prompt += f"What do you think we should add to this project? Which values need improving or editing?\n"
        prompt += f"Please respond in markdown format."
        
        print(colored(f"Prompt.to_assess_project_state: prompt set to \n{prompt}", "yellow"))
        
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
        dict, str = agent.to_dict_and_string()      
        prompt = f"Here is your character description: \n{str}"
        
        # print(colored(f"PromptBuilderSingleton().to_remind: prompt set to {prompt}", "yellow"))
        
        return self.auto_reminder(prompt, agent)  
