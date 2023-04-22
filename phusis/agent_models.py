import json, uuid, os
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .apis import *
from termcolor import colored
from django.db import models
from abc import ABC, abstractmethod
from .agent_attributes import *
from .agent_engines import AbstractEngine, OrchestrationEngine, PhusisScript, WritingAgentEngine, CompressionAgentEngine, EmbeddingsAgentEngine, WebSearchAgentEngine
from .agent_utils import get_user_agent_singleton, get_phusis_project_workspace


class File(models.Model):
    path_to_file = models.CharField(max_length=255)



class Vector(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    content = models.TextField(blank=False)
    embeddings = models.TextField(blank=False)
    
    def is_file(self):
        return os.path.isfile(self.data)



class AbstractAgent(models.Model, AbstractEngine, PhusisScript):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    agent_type = models.CharField(max_length=200, default="phusis_agent", editable=False)
    class_display_name = models.CharField(max_length=200, editable=False, default=f"Phusis {agent_type} Agent")
    related_books = GenericRelation('AgentBookRelationship', related_query_name='agent')
    awake = models.BooleanField(default=False)
    expose_rest = True
    # [{"prompted_by":"", "AgentCapability":{}, "result":""}]
    steps_taken = models.JSONField(default=list, blank=True)
    capabilities = models.ManyToManyField('AgentCapability', blank=True)
    embedding_of_self = models.TextField(blank=True)
    files_produced = models.ManyToManyField(File, blank=True,  related_query_name='produced_by')
    
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
    favored_genres = models.ManyToManyField(AgentFavoredGenre, blank=True)
    favored_genre_combos = models.ManyToManyField(AgentFavoredGenreCombo, blank=True)
    writing_style = models.ManyToManyField(AgentWritingStyle, blank=True)
    inspirational_sources = models.ManyToManyField(AgentInspirationalSource, blank=True)
    
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
        
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "agent_type": self.agent_type,
            "goals": [goal.name for goal in self.goals.all()],
            "roles": [role.name for role in self.roles.all()],
            "personality": [trait.name for trait in self.personality_traits.all()],
            "qualifications": [qual.name for qual in self.qualifications.all()],
            "impersonations": [imp.name for imp in self.impersonations.all()],
            "elaboration": self.elaboration,
            "steps_taken": self.steps_taken,
            "strengths": [strength.name for strength in self.strengths.all()],
            "possible_locations": [location.name for location in self.possible_locations.all()],
            "drives": [drive.name for drive in self.drives.all()],
            "fears": [fear.name for fear in self.fears.all()],
            "beliefs": [belief.name for belief in self.beliefs.all()],
            "age": self.age,
            "origin_story": self.origin_story,
            "llelle": self.llelle,
            "malig": self.malig,
            "subtr": self.subtr,
        }
        
    def introduce_yourself(self, is_brief=True):
        capability_id=17
        dict_str = json.dumps(self.to_dict(), indent=4)
        
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
    
    @abstractmethod
    def get_project_details(self, to='assess'):
        pass
    
    @abstractmethod
    def add_agents_to(self):
        pass
    
    @abstractmethod
    def get_agents_for(self):
        pass
    
    @abstractmethod
    def get_schema_for(self):
        pass

    @abstractmethod
    def serialized(self):
        pass




class OrchestrationAgent(AbstractAgent, OrchestrationEngine):
    class_display_name = "Orchestration Agent"
    agent_type = "orchestration_agent"
    # capabilities =  get_agent_capabilities_by_capability_ids([100,101,102,103])



class WritingAgent(AbstractAgent, WritingAgentEngine):
    agent_type = "writing_agent"
    class_display_name = "Writing Agent"



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



class WebSearchAgentSingleton(AbstractAgent, WebSearchAgentEngine):
    agent_type = "web_search_agent"
    class_display_name = "Web Search Agent"


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



class CharacterAgent(AbstractAgent):
    # agents that flesh out character profiles in various different genres, styles, target audience profiles, etc
    # also agents that become the character so that a user or other agents can talk to them, or to produce dialog
    agent_type = "character_agent"
    class_display_name = "Character Agent"
  


    
class WorldBuildingAgent(AbstractAgent):
    agent_type = "world_building_agent"
    class_display_name = "World Building Agent"

    
class ThemeExploringAgent(AbstractAgent):
    agent_type = "theme_exploring_agent"
    class_display_name = "Theme Exploring Agent"
    
    
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



def load_agent_model_and_return_instance_from(json_data):
    new_agent_obj = {}
    expected_json = {
        "class_name": "AgentsClassName",
        "properties": {
            "name": "Agent name"
        }
    }
 
    if is_valid_init_json(json_data):
        model_class = {}
        if json_data['class_name'] in globals():
            model_class = apps.get_model("phusis", f"{json_data['class_name']}")
        else: 
            print(colored(f"models.create_agent_model_from_instance: class_name {json_data['class_name']} not found in globals()", "red"))

        new_agent_obj, created = model_class.objects.update_or_create(name=json_data['properties']['name'])
        new_agent_obj.set_data(json_data['properties'])
        new_agent_obj.save()

        # new_agent_obj, created = model_class.objects.get_or_create(name=json_data['properties']['name'])
        # new_agent_obj.set_data(json_data['properties'])
        # new_agent_obj.save()
        s = "found and updated"
        if created: s = "created"
        print(colored(f"load_agent_model_and_return_instance_from: {new_agent_obj.name} {s}", "green"))
        
    else:
        print(colored(f"models.create_agent_model_from_instance: JSON data for agent not valid, expected schema below","red"))
        print(colored(f"Data received: {json_data}", "red"))
        print(colored(f"Minimum expected: {expected_json}", "yellow"))

    return new_agent_obj

