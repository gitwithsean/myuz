import json, uuid, os
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .apis import *
from termcolor import colored
from django.db import models
from abc import ABC, abstractmethod
from .agent_attributes import *
from .agent_engines import AbstractEngine, OrchestrationEngine, WritingAgentEngine, compress_text


class AbstractAgent(models.Model, AbstractEngine):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    agent_type = models.CharField(max_length=200, default="phusis_agent", editable=False)
    agent_system_prompt = models.TextField(blank=True)
    class_display_name = models.CharField(max_length=200, editable=False, default=f"Phusis {agent_type} Agent")
    related_books = GenericRelation('AgentBookRelationship', related_query_name='agent')
    project_attributes_assigned_to = models.ManyToManyField('PhusisProjectAttribute', blank=True)
    expose_rest = True
    # [{"prompted_by":"", "AgentCapability":{}, "result":""}]
    steps_taken = models.JSONField(default=list, blank=True)
    capabilities = models.ManyToManyField('AgentCapability', blank=True)
    embedding_of_self = models.TextField(blank=True)
    chat_logs = models.ManyToManyField('ChatLog', blank=True)
    awake = models.BooleanField(default=False)
    wake_up_message = models.TextField(blank=True, null=True)
    compressed_wake_up_message = models.TextField(blank=True, null=True)
    agent_assignments = models.ManyToManyField('AgentAssignment', blank=True, default=[], related_name='%(class)s_assignments')
    
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
        return f"{self.name}"        

        
    def add_to_chat_logs(self, prompt, response):
        
        print(colored(f"AbstractAgent.add_to_chat_logs: prompt:\n{prompt} \nresponse:\n{response}", "yellow"))
        
        new_chat_log = ChatLog(prompt=prompt, response=response, responder_name=self.name, responder_type=self.agent_type, responder_id=self.id)
        new_chat_log.save()
        self.save()
        self.chat_logs.add(new_chat_log)
        return new_chat_log
        
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

                # Find the related objects using find_agent_attribute_by function
                for attr_name in value:
                    # print(f"{field.related_model} {attr_name}")
                    attr_clas, attr_instance = find_agent_attribute_by(attr_name, field.related_model)
                    related_objects.append(attr_instance)

                # Set the related objects to the attribute
                getattr(self, key).set(related_objects)
            else:
                # Handle other attribute types as needed
                setattr(self, key, value)
        self.save()
        
    def to_dict_and_string(self):
        self_dict = {
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
        
        string_from_dict = f"\n### Name: {self_dict['name']}\n- Type: {self_dict['agent_type']}\n" 
        
        if self_dict['goals']: string_from_dict += f"- goals: {self_dict['goals']}\n" 
        
        if self_dict['roles']: string_from_dict += f"- roles: {self_dict['roles']}\n"
        
        if self_dict['personality']: string_from_dict += f"- personality: {self_dict['personality']}\n"
        
        if self_dict['qualifications']: string_from_dict += f"- qualifications {self_dict['qualifications']}\n"
        
        if self_dict['impersonations']: string_from_dict += f"- impersonations: {self_dict['impersonations']}\n"
        
        if self_dict['elaboration']: string_from_dict += f"- elaboration: {self_dict['elaboration']}\n"
        
        if self_dict['strengths']: string_from_dict += f"- strengths: {self_dict['strengths']}\n"
        
        if self_dict['possible_locations']: string_from_dict += f"- possible_locations: {self_dict['possible_locations']}\n"
        
        if self_dict['drives']: string_from_dict += f"- drives: {self_dict['drives']}\n"
        
        if self_dict['fears']: string_from_dict += f"- fears: {self_dict['fears']}\n"
        
        if self_dict['beliefs']: string_from_dict += f"- beliefs: {self_dict['beliefs']}\n"
        
        if self_dict['age']: string_from_dict += f"- age: {self_dict['age']}\n"
        
        if self_dict['origin_story']: string_from_dict += f"- origin_story: {self_dict['origin_story']}\n"
        
        if self_dict['llelle']: string_from_dict += f"- llelle: {self_dict['llelle']}\n"
        
        if self_dict['malig']: string_from_dict += f"- malig: {self_dict['malig']}\n"
        
        if self_dict['subtr']: string_from_dict += f"- subtr: {self_dict['subtr']}\n"
          
        string_from_dict = string_from_dict.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
         
        return self_dict, string_from_dict
        
    def introduce_yourself(self, is_brief=True):
        capability_id=17
        dict, str, embedding = self.to_dict_and_string()
        
        return f"Hi! I am an instance of the {self.agent_type} type of AI agent.\nHere are my basic attributes:\n{str}"


class ChatLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    prompt = models.TextField(blank=False, null=False)
    response = models.TextField(blank=False, null=False)
    compressed_prompt_content = models.TextField(blank=True, null=True, default='')
    compressed_response_content = models.TextField(blank=True, null=True, default='')
    responder_name = models.CharField(max_length=200, default='', blank=False, null=False)
    responder_type = models.CharField(max_length=200, default='', blank=False, null=False)
    responder_id = models.UUIDField(default=uuid.uuid4, auto_created=True, editable=False)
    
    def convert_log_to_chain_objects(self):
        # print(colored(f"ChatLog.convert_log_to_chain_objects(): right before compression, prompt is {self.prompt}", "yellow"))
        # print(colored(f"ChatLog.convert_log_to_chain_objects(): right before compression, response is {self.response}", "yellow"))
        
        if self.compressed_prompt_content == '' and self.prompt: self.compressed_prompt_content = compress_text(self.prompt, 0.25)
        if not self.compressed_response_content == '' and self.response: self.compressed_response_content = compress_text(self.response, 0.25)
        self.save()
        prompt_obj = {"role": "user", "content": f"{self.compressed_prompt_content}"}
        response_obj = {"role": "assistant", "content": f"{self.compressed_response_content}"}
        # return [prompt_obj, response_obj]
        return [prompt_obj]
  
    
class PhusisProjectAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)


class AgentAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    assignment_str = models.TextField(blank=True, null=True, default='')
    assignment_proj_att = models.ForeignKey(PhusisProjectAttribute, related_name='project_attribute_for_agent_assignment', on_delete=models.CASCADE, blank=True, null=True)
    additional_assignment_instructions = models.TextField(blank=True, null=True, default='')


class PhusisProjectGoalStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=1000, blank=False, null=False)
    related_project_attributes = models.ManyToManyField(PhusisProjectAttribute, related_name='project_attributes_for_project_goal_step', blank=True, default=[])
    agent_assignments_for_step = models.ManyToManyField(AgentAssignment, related_name='project_goal_steps_for_agent_assignment', blank=True, default=[])
    
    def add_agent_assignment_to_step(self, assignment_obj):
        agent_name = assignment_obj['agent_assigned']['agent_name']
        agent = AbstractAgent.objects.get(name=agent_name)
        new_assignment = AgentAssignment(agent_assigned=agent)
        
        if assignment_obj['assignment']['assignment_str']:
            new_assignment.assignment_str = assignment_obj['assignment']['assignment_str']
        
        if assignment_obj['assignment']['assignment_proj_att']:    
            new_assignment.assignment_proj_att = PhusisProjectAttribute.objects.get(name=assignment_obj['assignment']['assignment_proj_att'])
        
        if assignment_obj['additional_assignment_instructions']:
            new_assignment.additional_assignment_instructions = assignment_obj['additional_assignment_instructions']
        
        self.save()
        new_assignment.save()
        self.agent_assignments_for_step.add(new_assignment)
        self.save()
        
        return new_assignment
      
    def add_project_attributes_to_step(self, attributes):
        self.related_project_attributes.add(attributes)
        self.save()

class PhusisProjectGoal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=500, blank=False, null=False)
    steps = models.ManyToManyField(PhusisProjectGoalStep, blank=True, default=[])

    def add_steps_to_goal(self, steps):
        print(colored(f"PhusisProjectGoal.add_steps_to_goal: goal_name:\n{self.name} \nsteps_for_goal:\n{steps}", "yellow"))
        
        for step in steps:
            new_step = PhusisProjectGoalStep(name=step)
            self.save()
            new_step.save()
            self.steps.add(new_step)
            self.save()

class AbstractPhusisProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, default='')
    project_type = models.CharField(max_length=200, default='Book')
    project_user_input = models.TextField(blank=True, default='')
    project_workspace = models.CharField(max_length=200, default='', blank=True, null=True)
    goals_for_project = models.ManyToManyField(PhusisProjectGoal, blank=True, default=[])
    project_attributes = models.ManyToManyField(PhusisProjectAttribute, blank=True)
    agent_assignments_for_project = models.ManyToManyField(AgentAssignment, related_name='projects_for_agent_assignment', blank=True, default=[])
    
    project_embedding = models.TextField(blank=True)
    
    def add_to_goals_for_project(self, goals):
        print(colored(f"AbstractPhusisProject.add_to_goals_for_project: project: {self.name} goals:\n{goals}", "yellow"))
        
        for goal in goals:
            new_goal = PhusisProjectGoal(name=goal)
            new_goal.save()
            self.save()
            self.goals_for_project.add(new_goal)
            self.save()
    
    def __str__(self):
        return f"{self.project_type}: {self.name}"
    
    def project_attributes_to_md(self):
       atts_to_md = ""
       for attribute in self.project_attributes:
           atts_to_md = atts_to_md + f"- {attribute.name}\n"
       
       return atts_to_md
       
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
        
        # self.project_workspace = get_phusis_project_workspace(self.project_type, self.name)

        self.save()
    
    def convert_array_to_md_list(self, array):
        md_list=""
        for item in array:
            md_list += f"- {item}\n"
        
    @abstractmethod
    def list_project_attributes(self):
        pass
    
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
    def project_brief(self):
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
            cls._instance = super().__new__(cls)
        return cls._instance
    
    class Meta:
        ordering = None

    def save(self, *args, **kwargs):
        if not self.pk and UserAgentSingleton.objects.exists():
            raise ValueError("An instance of UserAgentSingleton already exists.")
        return super(UserAgentSingleton, self).save(*args, **kwargs)

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
            # print(colored(f"agent_models.create_agent_model_from_instance: class_name {json_data['class_name']} not found in globals()", "yellow"))
            pass
        new_agent_obj, created = model_class.objects.update_or_create(name=json_data['properties']['name'])
        
        new_agent_obj.set_data(json_data['properties'])
        s = "found and updated"
        if created: s = "created"
        # print(colored(f"agent_models.load_agent_model_and_return_instance_from: {new_agent_obj.name} {s}", "green"))
        
    else:
        print(colored(f"agent_models.create_agent_model_from_instance: JSON data for agent not valid, expected schema below","red"))
        print(colored(f"Data received: {json_data}", "red"))
        print(colored(f"Minimum expected: {expected_json}", "yellow"))

    return new_agent_obj


