import json, uuid, os, mimetypes, sys, PyPDF2, nltk, spacy, re
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.apps import apps
from .apis import *
from datetime import datetime
from termcolor import colored
from pprint import pprint
from django.db import models


class AbstractAgentAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, null=True, unique=True)
    agent_attribute_type = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True)
    expose_rest = True
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.agent_attribute_type} '{self.name}'"
    
    def set_data(self, properties_json):
        self.name = properties_json.get('name', self.name)
        self.elaboration = properties_json.get('elaboration', self.elaboration)
        self.save()
    
    def dictionary(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "agent_attribute_type": self.agent_attribute_type,
            "elaboration": self.elaboration
        }
        

class AgentCapability(AbstractAgentAttribute):
    capability_id = models.IntegerField(blank=False, null=False, default=-1)
    agent_attribute_type = "agent_capability" 
    prompt_adjst = models.TextField(blank=True, null=True)
    parameters = models.JSONField(blank=True, default=list)
    output_schema = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['capability_id']
        
    def __str__(self):
        return f"{self.capability_id}: {self.name}"

    def set_data(self, properties_json):
        self.name = properties_json.get('name', self.name)
        self.capability_id = properties_json.get('capability_id', self.capability_id)
        self.elaboration = properties_json.get('elaboration', self.elaboration)
        self.prompt_adjst = properties_json.get('prompt_adjst', self.prompt_adjst)
        self.parameters = properties_json.get('parameters', self.parameters)
        self.output_schema = properties_json.get('output_schema', self.output_schema)
        self.save()


class AgentGoal(AbstractAgentAttribute):
    agent_attribute_type = 'agent_goal'

class OrcAgentGoal(AgentGoal):
    agent_attribute_type = 'orc_agent_goal'

class AgentRole(AbstractAgentAttribute):
    agent_attribute_type = 'agent_role'

class OrcAgentRole(AgentRole):
    agent_attribute_type = 'orc_agent_role'

class AgentPersonalityTrait(AbstractAgentAttribute):
    agent_attribute_type = 'agent_personality_trait'

class OrcAgentPersonalityTrait(AgentPersonalityTrait):
    agent_attribute_type = 'orc_agent_personality_trait'

class AgentQualification(AbstractAgentAttribute):
    agent_attribute_type = 'agent_qualification'

class OrcAgentQualification(AgentQualification):
    agent_attribute_type = 'orc_agent_qualification'

class AgentImpersonation(AbstractAgentAttribute):
    agent_attribute_type = 'agent_impersonation'

class OrcAgentImpersonation(AgentImpersonation):
    agent_attribute_type = 'orc_agent_impersonation'

class AgentStrength(AbstractAgentAttribute):
    agent_attribute_type = 'agent_strength'

class OrcAgentStrength(AgentStrength):
    agent_attribute_type = 'orc_agent_strength'

class AgentLocation(AbstractAgentAttribute):
    agent_attribute_type = 'agent_location'

class OrcAgentLocation(AgentLocation):
    agent_attribute_type = 'orc_agent_location'

class AgentDrive(AbstractAgentAttribute):
    agent_attribute_type = 'agent_drive'

class OrcAgentDrive(AgentDrive):
    agent_attribute_type = 'orc_agent_drive'

class AgentFear(AbstractAgentAttribute):
    agent_attribute_type = 'agent_fear'

class OrcAgentFear(AgentFear):
    agent_attribute_type = 'orc_agent_fear'

class AgentBelief(AbstractAgentAttribute):
    agent_attribute_type = 'agent_belief'

class OrcAgentBelief(AgentBelief):
    agent_attribute_type = 'orc_agent_belief'

class AgentAttitude(AbstractAgentAttribute):
    agent_attribute_type = 'agent_belief'

class OrcAgentAttitude(AgentAttitude):
    agent_attribute_type = 'orc_agent_attitude'

class AgentFavoredTheme(AbstractAgentAttribute):
    agent_attribute_type = 'agent_favored_theme'
 
class OrcAgentFavoredTheme(AgentFavoredTheme):
    agent_attribute_type = 'orc_agent_favored_theme'

class AgentFavoredGenre(AbstractAgentAttribute):
   agent_attribute_type = 'agent_favored_genre'
        
class AgentFavoredGenreCombo(AbstractAgentAttribute):
    agent_attribute_type = 'agent_favored_genre_combo'        
        
class AgentInspirationalSource(AbstractAgentAttribute):
    agent_attribute_type = 'agent_inspirational_sources'         
        
class AgentCreatedTrait(AbstractAgentAttribute):
    agent_attribute_type = 'agent_created_trait'
    agent_created_trait_field = models.CharField(max_length=200, null=True, unique=True, default='')
    agent_created_trait_values = models.JSONField(null=True, blank=True, default=list)
    
    def set_data(self, properties_json):
        pprint(properties_json)
        print(properties_json.get('trait_field'))
        print(properties_json.get('trait_value'))
        self.agent_created_trait_field = properties_json.get('trait_field', self.agent_created_trait_field)
        self.agent_created_trait_values.append(properties_json.get('trait_value'))
        self.elaboration = properties_json.get('elaboration', self.elaboration)
        self.name = f"Agent Created Trait: {self.agent_created_trait_field}"
        self.save()

class OrcAgentCreatedTrait(AgentCreatedTrait):
    agent_attribute_type = 'orc_agent_created_trait'


def find_agent_attribute_by(attribute_name, attribute_class=AbstractAgentAttribute):
    if attribute_class == AgentCreatedTrait or attribute_class == OrcAgentCreatedTrait:
        attribute_name
    elif attribute_class == AbstractAgentAttribute:
        for att_class in AbstractAgentAttribute.model_subclasses().all():
            for instance in att_class.objects.all():
                if instance.name == attribute_name:
                    return att_class, instance
    else:
        for instance in attribute_class.objects.all():
            if instance.name == attribute_name:
                print(f"find_agent_attribute_by(): FOUND: {attribute_class}, {instance}")            
                return attribute_class, instance
           
    print(f"find_agent_attribute_by(): NOT FOUND: {attribute_class}, {attribute_name}")
    
    data = {
        "class_name": attribute_class.__name__,
        "properties":{
            "name": attribute_name
        }
    }

    return attribute_class, load_or_get_agent_attribute_from(data)
    
PROJECT_ROOT="myuz"
INCOMING_FILES="/files_to_embed/"
OUTGOING_FILES="/files_created/"
LOGS="/logs/"
def get_phusis_project_workspace(project_type, project_name):
    myuz_dir = os.getcwd()
    
    if PROJECT_ROOT in myuz_dir:
        myuz_dir = myuz_dir[:myuz_dir.index(PROJECT_ROOT) + len(PROJECT_ROOT)]
        
    phusis_project_workspace = f"{myuz_dir}/phusis/phusis_projects/{project_type}/{project_name}" 
        
    os.makedirs(f"{phusis_project_workspace}{INCOMING_FILES}", exist_ok=True)
    os.makedirs(f"{phusis_project_workspace}{OUTGOING_FILES}", exist_ok=True)
    os.makedirs(f"{phusis_project_workspace}{LOGS}", exist_ok=True)
    
    return phusis_project_workspace 

# see init_data/init_agent_capability.json
def get_agent_capabilities_by_capability_ids(capability_ids=
                                             [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]):

    capabilities = []
    for id in capability_ids:
        capability = AgentCapability.objects.get(capability_id=id)
        capabilities.append(capability)
 
    return capabilities


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


def is_valid(json_data):
    
    # print("HER LOOK HERE")
    # pprint(json_data)
    
    # print(f"{json_data['class_name']}")
    # print(f"{json_data['properties']}")
    # print(f"{json_data['properties']['name']}")
    if not 'class_name' in json_data or not 'properties' in json_data or not 'name' in json_data['properties']:
        return False
    else:
        return True


def load_or_get_agent_attribute_from(json_data):
    new_attribute_obj = {}
    expected_json = {
        "class_name": "AgentCapability",
        "properties": {
            "name": "Agent Capability name"
        }
    }
    
    if is_valid(json_data):
        attribute_class = apps.get_model("phusis", f"{json_data['class_name']}")
        if json_data['class_name'] == "AgentCreatedTrait" or json_data['class_name'] == "OrcAgentCreatedTrait":
            pprint(json_data)
            new_attribute_obj, created = attribute_class.objects.update_or_create(
                name=f"Agent Created Trait: {json_data['properties']['trait_field']}",
                defaults={
                    'agent_created_trait_field': json_data['properties']['trait_field'],
                    'agent_created_trait_values': json_data['properties']['trait_values']
                }
            )
            return new_attribute_obj
        else:        
            print(colored(f"load_or_get_agent_attributefrom(): Loading {json_data['properties']['name']}", "green"))
            new_attribute_obj, created = attribute_class.objects.get_or_create(name=json_data['properties']['name'])
            
            new_attribute_obj.set_data(json_data['properties'])
            
            s = "found and updated"
            if created: s = "created"
            print(colored(f"load_agent_attributes_from(): {new_attribute_obj.name} {s}", "green")) 
        
        # new_attribute_obj.save()
    else:
        print(colored(f"models.load_agent_attributes_from: JSON data for att not valid, expected schema below","red"))
        print(colored(f"Data received: {json_data}", "red"))
        print(colored(f"Minimum expected: {expected_json}", "yellow"))   
    
    return new_attribute_obj        
    

def load_agent_model_and_return_instance_from(json_data):
    new_agent_obj = {}
    expected_json = {
        "class_name": "AgentsClassName",
        "properties": {
            "name": "Agent name"
        }
    }
 
    if is_valid(json_data):
        model_class = {}
        if json_data['class_name'] in globals():
            model_class = apps.get_model("phusis", f"{json_data['class_name']}")
        else: 
            model_class = DynamicAgent
            json_data['properties']['agent_type'] = camel_case_to_underscore(json_data['class_name'])
            json_data['properties']['class_display_name'] = camel_case_to_spaced(json_data['class_name'])
        
        new_agent_obj, created = model_class.objects.get_or_create(name=json_data['properties']['name'])
        new_agent_obj.set_data(json_data['properties'])
        new_agent_obj.save()
        s = "found and updated"
        if created: s = "created"
        print(colored(f"load_agent_model_and_return_instance_from: {new_agent_obj.name} {s}", "green"))
        
    else:
        print(colored(f"models.create_agent_model_from_instance: JSON data for agent not valid, expected schema below","red"))
        print(colored(f"Data received: {json_data}", "red"))
        print(colored(f"Minimum expected: {expected_json}", "yellow"))

    return new_agent_obj


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
    
    def thoughts_concerns_proposed_next_steps(self, agent, agent_to_share_with):
        prompt = f"{agent_to_share_with}, {agent_to_share_with.agent_type} of the swarm you are a member of, has requested for you to report back. They want you to reflect on what you have done so far, and respond in the following format as concisely as possible:\n\nTHOUGHTS:\n\nCONCERNS\n\nWHAT YOU THINK YOUR NEXT STEPS SHOULD BE:\n\n"
        return self.auto_reminder(prompt, agent) 
    
    def to_remind(self, agent):      
        prompt = f"Here is your character description: {agent.dicctionary()}"
        
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



class PhusisScript():
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    # name = models.CharField(max_length=200) 
    # is_master_script = models.BooleanField(default=False)
    in_debug_mode = True
    #script as list of tuples speaker/spoken 
    # [ { date_time, speaker_id, speaker_name, content } ]
    script_content = models.TextField(blank=True, null=True, default='')
    class_display_name = 'Swarm Script'
    script_file_name = models.CharField(max_length=200, default="", editable=False)
    path_to_script = models.CharField(max_length=200, default="", editable=False)
    
    def __init__(self):
        self.path_to_script=f"{get_phusis_project_workspace(self.__class__.__name__, self.name)}{LOGS}"        
        self.script_file_name = self.script_file_name = f"{self.name}_script_{datetime.utcnow().strftime('%Y%m%d_%H%M')}"

    def script_to_text(self):
        txt = ""
        for entry in self.script_content:
            s = f"speaker_name: {entry.get('speaker_name', '')}\n"
            s = f"text: {entry.get('text', '')}\n\n"
            txt = f"{txt}\n\n{s}"
        return txt 

    def save_script_to_file(self):
        print(colored("Saving script to file...", "green"))

        with open(f"{self.path_to_script}{self.script_file_name}", "w") as f:
            json.dump({"script": {"script_entries": self.script_content}}, f, indent=4) 
        
    def add_script_entry(self, prompter, prompt, responder, response):
        capability_id=14
        time_stamp = datetime.utcnow().strftime("%Y.%m.%d.%H.%M.%s_%Z")
        prompt_and_response = {
            "time_stamp" : time_stamp,
            "prompt_entry" : {
                "is_prompt": True,
                "agent": f"{prompter.id}",
                "prompter_name": prompter.name,
                "time_stamp": time_stamp,
                "text": prompt
            },
            "response_entry" : {
                "is_prompt": False,
                "agent": f"{responder.id}",
                "responder_name": responder.name,
                "time_stamp": time_stamp,
                "text": response
            }
        }
        print(colored("Adding prompt_and_response script entry...", "green"))

        # Save the updated array back to the instance
        self.script_content = f"{self.script_content},\n{prompt_and_response}" 
        self.save()
        if self.in_debug_mode:
            pprint(prompt_and_response)
            
    def recent_script_entries(self, num_entries=5):
        capability_id=15
        print(colored(f"Retrieving {num_entries} most recent prompt_and_response script entries...", "green"))
        i = 0
        recent_entries = []
        if num_entries > len(self.script.script_content):
            num_entries = len(self.script.script_content)
        for entry in reversed(self.script.script_content):
            if i >= num_entries:
                break
            recent_entries.append(entry)
        print(colored(f"Retrieved {len(recent_entries)} recent prompt_and_response script entries.", "green"))
        return recent_entries



class Vector(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    content = models.TextField(blank=False)
    embeddings = models.TextField(blank=False)
    
    def is_file(self):
        return os.path.isfile(self.data)



class AbstractEngine():
    ai_api = OpenAi()
    agent = {}
    awareness = 'as_ai'
    expose_rest = True
    most_recent_responses_to = {
        "start_engine": "",
        "thoughts_concerns_proposed_next_steps": "",
        "submit_report": ""
    }
    # open_ai_data = {
    #     "role": "user",
    #     "content": "",
    #     "model": "text-ada-001",
    #     "temperature": 0.2,
    #     "max_tokens": 300,
    #     "top_p": 1,
    #     "frequency_penalty": 0,
    #     "presence_penalty": 0,
    # }
    open_ai_data = {
       'model':"text-curie-001",
       'max_tokens':1000
    }
    
    def submit_chat_prompt(self, prompt, prompting_agent):
        print(colored("Submitting chat prompt...", "green"))
        request_data = self.open_ai_data
        request_data['content'] = PromptBuilderSingleton().complete_prompt(prompt, prompting_agent)
        response = self.ai_api.gpt_chat_response(request_data)
        print(colored("Chat prompt submitted.", "green"))
        return prompt, response
        
    def start_engine(self):
        return self.wake_up()
    
    def wake_up(self):
        capability_id=0
        print(colored(f"Starting engine for {self.name}...", "green"))
        request_data = self.open_ai_data
        request_data['content'] = PromptBuilderSingleton().to_wake_up(self)
        response = self.ai_api.gpt_chat_response(request_data)
        self.awake = True
        self.most_recent_responses_to['start_engine'] = response
        print(colored(f"{self.name} engine started.", "green"))
        return request_data['content'], response

    def consider(self, objs=[], prompt_adj=''):
        capability_id=1
        pass

    def produce(self, objs=[], prompt_adj=''):
        capability_id=2
        pass

    def reflect_on(self, objs=[], prompt_adj=''):
        capability_id=3
        pass
    
    def question_criticize (self, objs=[], prompt_adj=''):
        capability_id=4
        pass
    
    def offer_prompts(self, objs=[], prompt_adj=''):
        capability_id=5
        pass
    
    def thoughts_concerns_propose_next_steps(self, agent_to_share_with):
        capability_id=6
        print(colored("Sharing thoughts, concerns, and proposed next steps...", "green"))
        request_data = self.open_ai_data
        request_data['content'] = PromptBuilderSingleton().thoughts_concerns_proposed_next_steps(self, agent_to_share_with)
        response = self.submit_chat_prompt(self, request_data['content'], agent_to_share_with)
        self.most_recent_responses_to['thoughts_concerns_proposed_next_steps'] = response
        print(colored("Thoughts, concerns, and proposed next steps shared.", "green"))
        return request_data['content'], response

    def submit_state_report_to(self, agent):
        capability_id=7
        print(colored("Submitting report...", "green"))
        request_data = self.open_ai_data
        report = self.report()
        request_data['content'] = self.compress_prompt(self, report, agent)
        response = self.submit_chat_prompt(self, request_data['content'], agent)
        self.most_recent_responses_to['report_to'] = response
        print(colored("Report submitted.", "green"))
        return request_data['content'], response

    def list_productions(self):
        capability_id=8
        pass

    def return_production_content(self):
        capability_id=9
        pass

    def executive_summary_of(self, obj=[]):
        capability_id=10
        if obj.len()==0: obj.append(self)
        pass
    
    def delve_into(self):
        capability_id=11
        pass
    
    def improvise_on(self, obj=[]):
        capability_id=12
        if obj.len()==0: obj.append(self)
        pass
    
    def dwell_on(self, obj=[]):
        capability_id=13
        if obj.len()==0: obj.append(self)
        pass
    
    def report_from(self):
        return {
            "agent_type": (self.agent_type, 'unknown_agent_type'),
            "name": self.name,
            "goals": list(self.goals.all().values_list('name', flat=True)),
            "roles": list(self.roles.all().values_list('name', flat=True)),
            "personality_traits": list(self.personality.all().values_list('name', flat=True)),
            "qualificatons": list(self.qualifications.all().values_list('name', flat=True)),
            "impersonations": list(self.impersonations.all().values_list('name', flat=True)),
            "self-summarization": (self.summarize_self(), ''),
        }
        
    def report(self):
        print(colored("Generating report...", "green"))
        report = {}
        if self.awake:
            report = {
                "report_from": self.report_from(),
                "awake": True,
                "report":{
                    "conext":{
                        "recent_script_entries": self.recent_script_entries(),
                        "steps_taken": self.list(self.steps_taken.all().values_list('name', flat=True))
                    },
                    "thoughts_concerns_proposed_next_steps": self.thoughts_concerns_proposed_next_steps()
                }
            }
        else:
            report = {
                "report_from": self.report_from(),
                "awake": False,
            }
        print(colored("Report generated.", "green"))
        return report



class AbstractAgent(models.Model, AbstractEngine, PhusisScript):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    # script_for_agent = models.OneToOneField('PhusisScript', null=True, blank=True, on_delete=models.PROTECT)
    agent_type = models.CharField(max_length=200, default="phusis_agent", editable=False)
    class_display_name = models.CharField(max_length=200, editable=False, default=f"Phusis {agent_type} Agent")
    related_books = GenericRelation('AgentBookRelationship', related_query_name='agent')
    awake = models.BooleanField(default=False)
    expose_rest = True
    # [{"prompted_by":"", "AgentCapability":{}, "result":""}]
    steps_taken = models.JSONField(default=list, blank=True)
    capabilities = models.ManyToManyField('AgentCapability', blank=True)
    # is_concerned_with =  models.ForeignKey('noveller.ConcreteNovellerModelDecorator', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_concerned_with_this')
    # is_influenced_by =  models.ForeignKey('noveller.ConcreteNovellerModelDecorator', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_influenced_by_this')
    embedding_of_self = models.TextField(blank=True)
    
    #Traits
    goals = models.ManyToManyField(AgentGoal, blank=True)
    roles = models.ManyToManyField(AgentRole, blank=True)
    personality_traits = models.ManyToManyField(AgentPersonalityTrait, blank=True)
    qualifications = models.ManyToManyField(AgentQualification, blank=True)
    impersonations = models.ManyToManyField(AgentImpersonation, blank=True)
    strengths = models.ManyToManyField(AgentStrength, blank=True)
    possible_locations = models.ManyToManyField(AgentLocation, blank=True)
    attitudes = models.ManyToManyField(AgentAttitude, blank=True)
    drives = models.ManyToManyField(AgentDrive, blank=True)
    fears = models.ManyToManyField(AgentFear, blank=True)
    beliefs = models.ManyToManyField(AgentBelief, blank=True)
    favored_themes = models.ManyToManyField(AgentFavoredTheme, blank=True)
    
    #Character
    age = models.IntegerField(null=True)
    origin_story = models.TextField(blank=True)
    elaboration = models.TextField(blank=True)
    llelle = models.TextField(blank=True)
    malig = models.TextField(blank=True)
    subtr = models.TextField(blank=True)  
    # [{"trait_name":"", "trait_values": ["",""]}]
    agent_created_traits = models.ManyToManyField(AgentCreatedTrait, blank=True)
    
    class Meta:
        abstract = True
        ordering = ['name']
    
    def __str__(self):
        return f"{self.class_display_name} for {self.name}"        

    def set_data(self, properties_dict):
        for key, value in properties_dict.items():
            # Get the field instance
            field = self._meta.get_field(key)

            #Deal with capabilities first
            if key == 'capabilities':
                self.capabilities.set(get_agent_capabilities_by_capability_ids()) 
                
            # Check if it's a ManyToManyField
            elif isinstance(field, models.ManyToManyField):
                related_objects = []

                # Find the related objects using find_attribute_by function
                for attr_name in value:
                    print(f"{field.related_model} {attr_name}")
                    attr_clas, attr_instance = find_agent_attribute_by(attr_name, field.related_model)
                    related_objects.append(attr_instance)

                # Set the related objects to the attribute
                getattr(self, key).set(related_objects)
            else:
                # Handle other attribute types as needed
                setattr(self, key, value)
    
    def embed(self):
        if self.embedding_of_self == '':
            self.embedding_of_self = EmbeddingsAgentSingleton.embed_agent(self)   
        
        return self.embedding_of_self
        
    def dictionary(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "agent_type": self.agent_type,
            "goals": self.goals,
            "roles": self.goals,
            "personality": self.goals,
            "qualifications": self.goals,
            "impersonations": self.goals,
            "elaboration": self.elaboration,
            "llelle": self.llelle,
            "malig": self.malig,
            "subtr": self.subtr,
            "steps_taken": self.steps_taken,
            "strengths": self.strengths,
            "possible_locations": self.possible_locations,
            "drives": self.drives,
            "fears": self.fears,
            "beliefs": self.beliefs,
            "age": self.age,
            "origin_story": self.origin_story,
            "agent_created_traits": self.agent_created_traits
        }
        
    def introduce_yourself(self, is_brief=True):
        capability_id=17
        dict_str = json.dumps(self.dictionary(), indent=4)
        
        return f"Hi! I am an instance of the {self.agent_type} type of AI agent.\nHere are my basic attributes:\n{dict_str}"

    def tell_me_who_i_am(self):
        you_are = f"You are a agent_type. "



class AbstractPhusisProject(models.Model, PhusisScript):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, default='', unique=True)
    project_type = models.CharField(max_length=200, default='Book')
    project_user_input = models.TextField(blank=True, default='')
    project_workspace = get_phusis_project_workspace(project_type, name)
    agents_for_project = models.ManyToManyField(
        AbstractAgent, related_name='projects_for_agent', blank=True
    )
    
    project_embedding = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.project_type}: {self.name}"
       
    class Meta:
        abstract = True
        ordering = ['name']
    
    def set_data(self, properties_dict):
        if self.script_for_project is None: 
            self.script_for_project = PhusisScript(is_script_for=self)
        for key, value in properties_dict.items():
            attr_type = type(getattr(self, key))
            if attr_type == list:
                getattr(self, key).append(value)
            else:
                setattr(self, key, value)
    
    def embed(self):
        if self.project_embedding == '':
            self.project_embedding = EmbeddingsAgentSingleton.embed_project(self)   
        
        return self.project_embedding
   


class CharacterAgent(AbstractAgent):
    # agents that flesh out character profiles in various different genres, styles, target audience profiles, etc
    # also agents that become the character so that a user or other agents can talk to them, or to produce dialog
    agent_type = "character_agent"
    class_display_name = "Character Agent"
  
  
  
 
#AGENTS WITH ENGINES
class OrchestrationEngine(AbstractEngine):
    auto_mode = False
    open_ai_data = {
       'model':"gpt-3.5-turbo",
       'max_tokens':1000
    }
    awareness = 'as_leader_of_ai_swarm'
    current_agent_states = []
          
    def assess_project(self, project_details):
        capability_id=100
        self.assess_agent_swarm()
        recent_script = self.recent_script_entries(10)
        recent_responses = self.most_recent_responses_to
        prompt = f"What is your current assessment of the project?\n\n"
        prompt = prompt + f"recent chats: {recent_script}\n\n"
        prompt = prompt + f"project details: {project_details}"
        prompt = prompt + f"recent responses: {recent_responses}"
        prompt = prompt + f"reports from agents: {self.current_agent_states}" 
        
        compressed_prompt = CompressionAgentSingleton().compress_prompt(prompt, 0.7)
        print(colored("Assessing project...", "green"))
        response = self.submit_chat_prompt(compressed_prompt, UserAgentSingleton())
        self.most_recent_responses_to['assess_project'] = response
        return response
    
    def assess_agent_swarm(self):
        capability_id=101
        print(colored("Assessing agent swarm...", "green"))

        # Get all the models from the phusis app
        phusis_models = apps.get_app_config('phusis').get_models()

        # Filter the models that are subclasses of AbstractAgent
        agent_models = [model for model in phusis_models if issubclass(model, AbstractAgent)]

        # Iterate over the agent models and get their reports
        for agent_model in agent_models:
            agent_instances = agent_model.objects.all()
            for agent_instance in agent_instances:
                print(colored(f"Getting report from agent: {agent_instance.name}", "green"))
                self.current_agent_states.append(agent_instance.report_from())
        print(colored("Finished assessing agent swarm.", "green"))
        
    def amend_project(self, project_details):
        capability_id=102
        prompt = prompt + f"\n\nHere is your most recent assessment of the project:\n\n{self.most_recent_responses_to['assess_project']}"
        prompt = prompt + f"\n\nHere is a user created introduction to the project: {project_details}"
        prompt = prompt + "\n\nGiven your most recent assessment of the project above, what do you think, given your expertise as an orchestrations agent, we need to do next? You have a variety of options, including, but not limited to.\nRequesting to wake up an agent and tasking them\nGiving new tasks to already awake agents\nAsking the User for more input\nWhatever else it is you think we could be doing to further the project\n"
        
        prompt = prompt + f"And as a reminder, this is who you are:\n\n{self.original_data}"
        
        compressed_prompt = CompressionAgentSingleton().compress_prompt(prompt, 0.5)
        print(colored("Amending project...", "green"))
        response = self.ai_api.submit_chat_prompt(self, compressed_prompt, UserAgentSingleton())
        self.most_recent_responses_to['amend_project'] = response
        return compressed_prompt, response
          
    def resume_project(self):
        capability_id=103
        print(colored("Resuming project...", "green"))
        #for now, just print the data so we can assess it!
        print(self.most_recent_responses_to['amend_project'])



class OrchestrationAgent(AbstractAgent, OrchestrationEngine):
    class_display_name = "Orchestration Agent"
    agent_type = "orchestration_agent"
    # capabilities =  get_agent_capabilities_by_capability_ids([100,101,102,103])



class WritingAgentEngine(AbstractEngine):
    pass



class WritingAgent(AbstractAgent, WritingAgentEngine):
    agent_type = "writing_agent"
    class_display_name = "Writing Agent"
    favored_themes = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    favored_genres = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    favored_genre_combinations = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    inspirational_sources = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    preferred_writing_style = ArrayField(models.CharField(max_length=50), blank=True, default=list)



class CompressionAgentEngine(AbstractEngine):
    open_ai_data = {
        "role": "user",
        "content": "",
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 1000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    
    def compress_prompt(self, prompt, compression_ratio='', prompting_agent={}):
        capability_id=18
        if prompting_agent == {}: prompting_agent = UserAgentSingleton()
        request_data = self.open_ai_data
        request_data['content'] = PromptBuilderSingleton().to_compress(prompt, compression_ratio)
        print(colored("Compressing prompt...", "green"))
        return self.submit_chat_prompt(prompt, prompting_agent)



class CompressionAgentSingleton(AbstractAgent, CompressionAgentEngine):
    agent_type = "compression_agent"
    class_display_name = "Compression Agent"
    _instance = None
    expose_rest = False
    capabilities = [18]
    def __new__(cls):
        if cls._instance is None:
            # print('Creating PromptBuilder singleton instance')
            cls._instance = super().__new__(cls)
            # Initialize the class attributes here
            cls._instance.prompts_since_reminder = 0
            cls._instance.max_prompts_between_reminders = 5
        return cls._instancee



class EmbeddingsAgentEngine(AbstractEngine):
    pinecone_api = PineconeApi()
    file_size_limit = 3     # in MB
    open_ai_data = {
        "model": "text-embedding-ada-002"
    }
    
    def receive_files(self, files):
        loaded_files = []
        
        for this_file in files:
            if not os.path.isdir(this_file):
                file_size = os.path.getsize(this_file) / (1024 * 1024) # Convert size to MB
                if file_size < self.file_size_limit:                    
                    loaded_files.append(self.read_file_into_mem(this_file))           
                else:
                    pass
                    #return error about this file
                    #or break it up into chunks
            else:
                print(colored(f"EmbeddingsAgentEngine.receive_files(): skipping {this_file}, we do not currently support loading from sub directories", "yellow"))
        
        return loaded_files            
    
    def read_file_into_mem(self, file):
        
        read_mode = 'r' #default for text files
        file_content = ""
        file_type, encoding = mimetypes.guess_type(file)
        
        if file_type == "application/pdf":
            read_mode = 'rb'    #for binary files
            
        with open(file, read_mode) as f:
            if(file_type == "application/pdf"):                 # Handling PDF files
                pdf_reader = PyPDF2.PdfFileReader(f)
                for i in range(pdf_reader.getNumPages()):
                    page = pdf_reader.getPage(i)
                    file_content += page.extractText()
            else:                                               # Handling basic text files
                file_content = f.read()
            
        return {"file_type": file_type, "local_file_path": os.path.abspath(file), "content": file_content}
       
    def tokenize_text(self, text):
        text_size = sys.getsizeof(text)  # Get the size of the text in bytes

        if text_size < 1024 * 1024:  # If the text size is less than 1 MB, use NLTK
            sentences = nltk.sent_tokenize(text)
        else:  # If the text size is 1 MB or more, use spaCy            
            # Load spaCy's English model
            nlp = spacy.load("en_core_web_sm")  
            doc = nlp(text)
            sentences = [sent.text for sent in doc.sents]

        return sentences
    
    def create_embeddings_for(self, data):
        capability_id=16
        texts_to_embed = []
        if isinstance(data, str):       # if data is a string, add string to texts_to_embed array
            print(colored(f"EmbeddingsAgentEngine.create_embeddings_for(): Loading text to embed...", "green"))
            texts_to_embed.append(data)      
        elif 'files' in data:           # if data is list of files, process and set as texts_to_embed array
            print(colored(f"EmbeddingsAgentEngine.create_embeddings_for(): Loading list of files to embed...", "green"))
            texts_to_embed = self.receive_files(data['files'])   
        elif 'texts' in data:           # if list of texts, set as texts_to_embed
            print(colored(f"EmbeddingsAgentEngine.create_embeddings_for(): Loading list of texts to embed...", "green"))
            texts_to_embed = (data['texts'])   
        else:
            error_msg = """
            ERROR in EmbeddingAgentEngine.create_embeddings_for()
            Incorrect input type for function create_embeddings_for
            Accepted inputs:
                data : { files : ["list", "of", "file", "paths", "for", "embedding"] }
                data : { texts : ["list", "of", "texts", "for", "embedding"] }
                data : "single text for embedding"
            Received input:\n
            """
            print(colored(error_msg, "red"))
            pprint(data)

        #process text, get embeddings, upsert to pinceone
        for text_data in texts_to_embed:             #TODO parallelization? maybe too many api calls
            print(colored(f"EmbeddingsAgentEngine.create_embeddings_for(): tokenizing text(s)...", "green"))
            text_data['tokenized_content'] = self.tokenize_text(text_data['content'])            
            print(colored(f"EmbeddingsAgentEngine.create_embeddings_for(): getting embeddings for tokenized text...", "green"))
            text_data['embeddings'] = self.ai_api.get_embedding_for(text_data['tokenized_content'])
            print(colored(f"EmbeddingsAgentEngine.create_embeddings_for(): upserting embeddings to pinecone and adding to local db...", "green"))
            self.pinecone_api.upsert_embedding(text_data)
        
    def embed_files_from_dir(self, dir_path='./phusis/files_to_embed/'):
        capability_id=17
        print(colored(f"EmbeddingsAgentEngine.embed_files_from_dir(): Embedding files in {dir_path}", "green"))
        file_list = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
        self.create_embeddings_for({'files': file_list})
    
 
 
class EmbeddingsAgentSingleton(AbstractAgent, EmbeddingsAgentEngine):
    name = "Embeddings Agent"
    agent_type = "embeddings_agent"
    class_display_name = "Embeddings Agent"
    expose_rest = False
    capabilities = [{"capability_id":16},{"capability_id":17}]
    
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            # print('Creating EmbeddingsAgentSingleton singleton instance')
            cls._instance = super().__new__(cls)
            # Initialize the class attributes here
            cls._instance.prompts_since_reminder = 0
            cls._instance.max_prompts_between_reminders = 5
        return cls._instance
    
    class Meta:
        ordering = None



class WebSearchAgentEngine(AbstractEngine):
    pass       



class WebSearchAgentSingleton(AbstractAgent, WebSearchAgentEngine):
    agent_type = "web_search_agent"
    class_display_name = "Web Search Agent"



#Available Agents for dynamic creation
class PoeticsAgent(AbstractAgent):
    """
    Agent class concerned with:
        * narrative technique
        * poetic literacy
        * literary/linguistic theory
        * metaphoric / analogistic approaches to the content 
    """
    agent_type = "poetics_agent"
    class_display_name = "Poetics Agent"
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.UUIDField(null=True, blank=True)  # id of the project it is assigned to
    projects_assigned_to = GenericForeignKey('content_type', 'object_id')
    


class StructuralAgent(AbstractAgent):
    # story plotting
    # story structure (r.g. experimental and/or tried and tested structures)
    # fleshing out the story structure and plotting based on the inputs from other agents in the swarm  
    agent_type = "structural_agent"
    class_display_name = "Structural Agent"


 
class ResearchAgent(AbstractAgent):
    # taking a subject area and a project goal, and thinking of research topics that could be researched for the book, 
    # how to plan, structure and initially approach that research
    # like an expert librarian, knowing or knowing how to find the best sources for researching a topic
    # doing the background research on those specific topics to an expert degree
    agent_type = "research_agent"
    class_display_name = "Research Agent"

    
class WorldBuildingAgent(AbstractAgent):
    agent_type = "world_building_agent"
    class_display_name = "World Building Agent"

    
class ThemeExploringAgent(AbstractAgent):
    agent_type = "theme_exploring_agent"
    class_display_name = "Theme Exploring Agent"
    themes = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    
    
class ConflictAndResolutionAgent(AbstractAgent):
    agent_type = "conflict_and_resolution_agent"
    class_display_name = "Conflict And Resolution Agent"
    
    
class InterdisciplinaryAgent(AbstractAgent):
    # These are relatively neutral agents that would consider the output from all agents in a swarm and make sure they are not deviating from each other, making sure that each of them are serving towards a common goal in a cohesive way, that research informs setting, informs themes, informs style etc. Not quite like a director of a film, more like assistant directors
    # They will provide 'grades' to what is produced, but less about quality and more about how close they are to cohering with the work of the other agents working in different disciplines. With 0.5 being neutral, 1 being exemplary and 0 meaning heading in the wrong direction.
    # 'impersonations' is less important with these agents, however let's add a field for 'personality' here, with personality traits that would help with their goals. These personality traits can be similar across each agent    
    agent_type = "interdisciplinary_agent"
    class_display_name = "Interdisciplinary Agent"


class QualityEvaluationAgent(AbstractAgent):
    # evaluating the output and work of each of the agents.
    # here is a list of each agent
    agent_type = "qualitye_valuation_agent"
    class_display_name = "Quality Evaluation Agent"


class DynamicAgent(AbstractAgent):
    # If any of the 'manager' agents feels there is a class of agent missing that they need
    #A list of tuples: { trait_field, trait_valuess [] }
    agent_created_attributes = []
    class_display_name = "Agent Created Agent"


class UserAgentSingleton(AbstractAgent):
    name = "user"
    agent_type = "user_agent"
    class_display_name = 'User'
    _instance = None
    expose_rest = False
    def __new__(cls):
        if cls._instance is None:
            # print('Creating PromptBuilder singleton instance')
            cls._instance = super().__new__(cls)
            # Initialize the class attributes here
            cls._instance.prompts_since_reminder = 0
            cls._instance.max_prompts_between_reminders = 5
        return cls._instance
    
    class Meta:
        ordering = None


class AgentBookRelationship(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    agent = GenericForeignKey('content_type', 'object_id')
    book = models.ForeignKey("noveller.Book", on_delete=models.CASCADE)

