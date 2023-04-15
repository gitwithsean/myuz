import json, uuid
from django.db import models
from abc import abstractmethod
from noveller.models import ConcreteNovellorModelDecorator
from .openai_api import OpenAi
from datetime import datetime
from pprint import pprint

#AGENT ENGINES
class AbstractEngine():
    ai_api = OpenAi()
    auto_mode = False
    awareness = 'as_ai'
    #defaults
    open_ai_data = {
        "role": "user",
        "content": "",
        "model": "text-ada-001",
        "temperature": 0.2,
        "max_tokens": 300,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    
    def start_engine(self, ):
        request_data = self.open_ai_data
        request_data['content'] = PromptBuilder().to_wake_up(self)
        return self.ai_api(request_data)
        
    def submit_chat_prompt(self, prompt, prompting_agent):
        request_data = self.open_ai_data
        request_data['content'] = PromptBuilder().complete_prompt(prompt, prompting_agent)
        return self.ai_api(request_data)


class OrchestrationEngine(AbstractEngine):
    open_ai_data = {
       'model':"gpt-3.5-turbo",
       'max_tokens':1000
    }
    awareness = 'as_leader_of_ai_swarm'

#ORCHESTRATION AGENT
class OrchestrationAgent(OrchestrationEngine):
    #OBJECTIVE ORIENTED TRAITS
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, default="")
    agent_type = "orchestration_agent"
    original_data = {}
    goals = models.ManyToManyField('OrcAgentGoal', blank=True)
    roles = models.ManyToManyField('OrcAgentRole', blank=True)
    qualifications = models.ManyToManyField('OrcAgentQualification', blank=True)
    elaboration = models.TextField(blank=True)
    
    #CHARACTER_TRAITS
    orc_character_age = models.IntegerField(null=True)
    orc_character_possible_locations = models.JSONField(default=list, blank=True)
    orc_character_personality_traits = models.ManyToManyField('OrcAgentTrait', blank=True)
    orc_character_impersonations = models.ManyToManyField('OrcAgentImpersonation', blank=True)
    orc_character_attitudes = models.JSONField(default=list, blank=True)
    orc_character_strengths = models.JSONField(default=list, blank=True)
    orc_character_drives = models.JSONField(default=list, blank=True)
    orc_character_fears = models.JSONField(default=list, blank=True)
    orc_character_beliefs = models.JSONField(default=list, blank=True)
    orc_character_origin_story = models.TextField(blank=True)
    orc_character_llelle = models.TextField(blank=True)
    orc_character_malig = models.TextField(blank=True)
    orc_character_subtr = models.TextField(blank=True)
    
    #AGENT CREATED DATA
    agent_created_traits = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return self.name
    
    def introduction(self):
        return AbstractAgent.introduction(self)
    
    def dictionary(self):
        return {
            "name": self.name,
            "agent_type": self.agent_type,
            "goals": self.goals,
            "roles": self.roles,
            "personality_traits": self.personality_traits,
            "qualifications": self.qualifications,
            "impersonations": self.impersonations,
            "elaboration": self.elaboration           
        }

#AGENTS
class AbstractAgent(models.Model, AbstractEngine):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, default="")
    agent_type = models.CharField(max_length=200, default="", editable=False)
    goals = models.ManyToManyField('AgentGoal', blank=True)
    roles = models.ManyToManyField('AgentRole', blank=True)
    personality_traits = models.ManyToManyField('AgentTrait', blank=True)
    qualifications = models.ManyToManyField('AgentQualification', blank=True)
    impersonations = models.ManyToManyField('AgentImpersonation', blank=True)
    is_concerned_with =  models.ForeignKey('noveller.ConcreteNovellorModelDecorator', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_concerned_with_this')
    is_influenced_by =  models.ForeignKey('noveller.ConcreteNovellorModelDecorator', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_influenced_by_this')
    embedding_of_self = models.TextField(blank=True)
    elaboration = models.TextField(blank=True)
    llelle = models.TextField(blank=True)
    malig = models.TextField(blank=True)
    subtr = models.TextField(blank=True)  
    script = models.OneToOneField('Script', null=True, blank=True, on_delete=models.PROTECT)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    
    def dictionary(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "agent_type": self.agent_type,
            "goals": list(self.goals.all().values_list('name', flat=True)),
            "roles": list(self.roles.all().values_list('name', flat=True)),
            "personality": list(self.personality.all().values_list('name', flat=True)),
            "qualifications": list(self.qualifications.all().values_list('name', flat=True)),
            "impersonations": list(self.impersonations.all().values_list('name', flat=True)),
            "elaboration": self.elaboration,
            "llelle": self.llelle,
            "malig": self.malig,
            "subtr": self.subtr
        }
        
    def introduction(self):
        dict_str = json.dumps(self.dictionary(), indent=4)
        
        return f"Hi! I am an instance of the {self.agent_type} type of AI agent.\nHere are my basic attributes:\n{dict_str}"

class UserAgent(AbstractAgent):
    name = "user"
    agent_type = "user_agent"
    
class ConcreteAgent(AbstractAgent):
    is_concerned_with = models.ForeignKey(ConcreteNovellorModelDecorator, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)sagents_concerned_with_this')
    is_influenced_by = models.ForeignKey(ConcreteNovellorModelDecorator, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)sagents_influenced_by_this')
    
    script = models.OneToOneField('Script', editable=False, on_delete=models.PROTECT, related_name='concrete_agent_for_script', null=True, blank=True,)
    
    class Meta:
        db_table = 'phusis_concrete_agent'

class PoeticsAgent(AbstractAgent):
    # narrative technique
    # poetic literacy
    # literary/linguistic theory
    # exploring themes
    # metaphoric / analogistic approaches to the content 
    agent_type = "poetics_agent"

class StructuralAgent(AbstractAgent):
    # story plotting
    # story structure (r.g. experimental and/or tried and tested structures)
    # fleshing out the story structure and plotting based on the inputs from other agents in the swarm  
    agent_type = "structural_agent"

class CharacterAgent(AbstractAgent):
    # agents that flesh out character profiles in various different genres, styles, target audience profiles, etc
    # also agents that become the character so that a user or other agents can talk to them, or to produce dialog
    agent_type = "character_agent"
 
class ResearchAgent(AbstractAgent):
    # taking a subject area and a project goal, and thinking of research topics that could be researched for the book, 
    # how to plan, structure and initially approach that research
    # like an expert librarian, knowing or knowing how to find the best sources for researching a topic
    # doing the background research on those specific topics to an expert degree
    agent_type = "research_agent"
    
class WorldBuildingAgent(AbstractAgent):
    agent_type = "world_building_agent"
    
class ThemeExploringAgent(AbstractAgent):
    agent_type = "theme_exploring_agent"
    
class ConflictAndResolutionAgent(AbstractAgent):
    agent_type = "conflict_and_resolution_agent"
    
class InterdisciplinaryAgent(AbstractAgent):
    # These are relatively neutral agents that would consider the output from all agents in a swarm and make sure they are not deviating from each other, making sure that each of them are serving towards a common goal in a cohesive way, that research informs setting, informs themes, informs style etc. Not quite like a director of a film, more like assistant directors
    # They will provide 'grades' to what is produced, but less about quality and more about how close they are to cohering with the work of the other agents working in different disciplines. With 0.5 being neutral, 1 being exemplary and 0 meaning heading in the wrong direction.
    # 'impersonations' is less important with these agents, however let's add a field for 'personality' here, with personality traits that would help with their goals. These personality traits can be similar across each agent    
    agent_type = "interdisciplinary_agent"

class QualityEvaluationAgent(AbstractAgent):
    # evaluating the output and work of each of the agents.
    # here is a list of each agent
    agent_type = "qualitye_valuation_agent"

class AgentCreatedAgents(AbstractAgent):
    # If any of the 'manager' agents feels there is a class of agent missing that they need
    #A list of tuples: { trait_field, trait_valuess [] }
    agent_created_attributes = []
        
#UTILITY AGENTS  
class WebSearchAgent(AbstractAgent):
    agent_type = "web_search_agent"
       
class CompressionAgent(AbstractAgent):
    agent_type = "compression_agent"
 
#AGENT ATTRIBUTES
class AbstractAgentAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, null=True)
    agent_attribute_type = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    
    def dictionary(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "agent_attribute_type": self.agent_attribute_type,
            "elaboration": self.elaboration
        }

class AgentGoal(AbstractAgentAttribute):
    agent_attribute_type = "agent_goal"
    
class AgentRole(AbstractAgentAttribute):
    agent_attribute_type = "agent_role"

class AgentTrait(AbstractAgentAttribute):
    agent_attribute_type = "agent_trait"
    
class AgentQualification(AbstractAgentAttribute):
    agent_attribute_type = "agent_qualification" 
    
class AgentImpersonation(AbstractAgentAttribute):
    agent_attribute_type = "agent_impersonation" 

#ORCHESTRATION AGENT ATTRIBUTES
class OrcAgentGoal(AgentGoal):
    agent_attribute_type = "orchestration_agent_goal"
    
class OrcAgentRole(AgentRole):
    agent_attribute_type = "orchestration_agent_role"

class OrcAgentTrait(AgentTrait):
    agent_attribute_type = "orchestration_agent_trait"
    
class OrcAgentQualification(AgentQualification):
    agent_attribute_type = "orchestration_agent_qualification" 
    
class OrcAgentImpersonation(AgentImpersonation):
    agent_attribute_type = "orchestration_agent_impersonation" 
        
#SCRIPTS
class Script(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, default="") 
    is_master_script = models.BooleanField(default=False)
    file_name = models.CharField(max_length=200)
    #script as list of tuples speaker/spoken 
    # [ { date_time, speaker_id, speaker_name, content } ]
    content = models.JSONField(default=list, blank=True)
    
    def __init__(self):
        self.file_name = f"master_script_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.json"
           
    def script_to_text(self):
        txt = ""
        for entry in self.content:
            s = f"speaker_name: {entry.get('speaker_name', '')}\n"
            s = f"text: {entry.get('text', '')}\n\n"
            txt = f"{txt}\n\n{s}"
        return txt 
    
    def add_entry(self, sender, prompt, receiver, response):
        time_stamp = datetime.utcnow().strftime("%Y%m%d_%H:%M_%Z")
        prompt_entry = {
            "is_prompt": True,
            "agent": sender.id,
            "speaker_name": sender.name,
            "time_stamp": time_stamp,
            "text": prompt
        }
        response_entry = {
            "is_prompt": False,
            "agent": receiver.id,
            "speaker_name": receiver.name,
            "time_stamp": time_stamp,
            "text": response
        }
        self.content.append(prompt_entry)
        self.content.append(response_entry)
        self.save_script_to_file()

    def save_script_to_file(self):
        file_name = f"master_script_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(file_name, "w") as f:
            json.dump({"script": {"script_entries": self.content}}, f)

#singleton
class PromptBuilder():
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            print('Creating PromptBuilder singleton instance')
            cls._instance = super().__new__(cls)
            # Initialize the class attributes here
            cls._instance.prompts_since_reminder = 0
            cls._instance.max_prompts_between_reminders = 5
        return cls._instance
    
    def complete_prompt(self, prompt, prompter):
        prompt = f"The following prompt comes from a {prompter.agent_type}:\n\n--------------------\n\n{prompt}"
        return self.auto_reminder(prompt)
    
    def auto_reminder(self, prompt):
        self.prompts_since_reminder = self.prompts_since_reminder + 1
        if self.prompts_since_reminder >= 5:
            prompt = f"{prompt} Just Reminding you: {self.to_remind()}"
            self.prompts_since_reminder = 0
        return f"{prompt}"
                        
    def to_wake_up(self, agent):
        if agent.awareness      =='as_bot':
            s=f"a {agent.agent_type}, part of a swarm of agents, each with a very defined set of attributes."
        elif agent.awareness    =='as_orc':
            s=f"the master orchestrator of a swarm of GPT agents, all working towards a common objective." 
        else:                          
            s="I'm glad to have your expertise on this project."
        
        prompt = f"You are {agent.name}, {s}. You will use your skills to the BEST of your ability to serve me, the human user, I will tell you our objective soon, but first, about you. {self.to_remind()}"

        return self.auto_reminder(prompt)  
    
    def to_remind(self, agent):      
        prompt = f"Here is your character description: {agent.dictionary()}"
        
        return self.auto_reminder(prompt)  

    def to_ask_opinion_about(self, it, agent):
        prompt = ""

        return self.auto_reminder(prompt) 
    
    def to_ask_next_step(self, agent):
        prompt = ""
        
        return self.auto_reminder(prompt)
    
    def to_ask_reflect_on(self, it):
        prompt = ""
        
        return self.auto_reminder(prompt)
