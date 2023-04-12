import inspect
from django.db import models

import uuid
from noveller.models import *

#PROMPTS
class PromptType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
class Prompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    prompt_type = models.ForeignKey('PromptType', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)    

    def __str__(self):
        return self.name


#AGENTS
class AgentSwarm():
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    agents = models.ManyToManyField('Agent')
    swarm_goals = models.ManyToManyField('AgentGoal')

    def __str__(self):
        return self.name

class Agent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200, default="")
    agent_type = models.CharField(max_length=200, default="", editable=False)
    goals = models.ManyToManyField('AgentGoal')
    roles = models.ManyToManyField('AgentRole')
    personality = models.ManyToManyField('AgentTrait')
    qualifications = models.ManyToManyField('AgentQualification')
    introduction = models.TextField(blank=True)
    subtr = models.TextField(blank=True)
    elaboration = models.TextField(blank=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    
    def dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "agent_type": self.agent_type,
            "goals": self.goals,
            "roles": self.roles,
            "personality": self.personality,
            "qualifications": self.qualifications,
            "introduction": self.introduction,
            "subtr": self.subtr,
            "elaboration": self.elaboration
        }

class OrchestrationAgent(Agent):
    introduction = "Hi! I am an orchestration agent. My role is..." # TODO

class PoeticsAgent(Agent):
    introduction = "Hi! I am a PoeticsAgent. My role is..." # TODO
    
class StructuralAgent(Agent):
    introduction = "Hi! I am a StructuralAgent. My role is..." # TODO
     
class CharacterAgent(Agent):
    introduction = "Hi! I am a CharacterAgent. My role is..." # TODO 
    
class ResearchAgent(Agent):
    introduction = "Hi! I am a ResearchAgent. My role is..." # TODO 
    
class WorldBuildingAgent(Agent):
    introduction = "Hi! I am a WorldBuildingAgent. My role is..." # TODO 
    
class ThemeExploringAgent(Agent):
    introduction = "Hi! I am a ThemeExploringAgent. My role is..." # TODO 
    
class ConflictAndResolutionAgent(Agent):
    introduction = "Hi! I am a ConflictAndResolutionAgent. My role is..." # TODO 
    
class InterdisciplinaryAgent(Agent):
    introduction = "Hi! I am a InterdisciplinaryAgent. My role is..." # TODO 
    
class QualityEvaluationAgent(Agent):
    introduction = "Hi! I am a QualityEvaluationAgent. My role is..." # TODO  
        
class WebSearchAgent(Agent):
    introduction = "Hi! I am a WebSearchAgent. My role is..." # TODO  
       
class CompressionAgent(Agent):
    introduction = "Hi! I am a CompressionAgent. My role is..." # TODO 
    
#AGENT ATTRIBUTES

class AbstractAgentAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    agent_attribute_type = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def dictionary(self):
        return {
            "id": self.id,
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

def get_instances_of_subclasses(base_class):
    # Get all subclasses of the given base class
    subclasses = []
    for subclass in base_class.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_instances_of_subclasses(subclass))
        
    # Create a new list of instances
    instances = []
    for subclass in subclasses:
        for name, obj in inspect.getmembers(subclass):
            if inspect.isclass(obj) and not inspect.isabstract(obj):
                instances.append(obj())
    
    return instances


#testing
def __main__():
    
    agent_goal = AgentGoal(name="My Goal1", elaboration="Description of my goal1.")
    agent_Role = AgentRole(name="My Role1", elaboration="Description of my role1.")
    agent_Role = AgentRole(name="My Role2", elaboration="Description of my role2.")
    agent_Role = AgentRole(name="My Role3", elaboration="Description of my role3.")
    Compression_agent = CompressionAgent(
        name="", 
        goals="", 
        roles="", 
        personality="", 
        qualifications="", 
        elaboration="", 
        subtr="", 
        agent_type=""
        )
    Interdisciplinary_agent = InterdisciplinaryAgent(
        name="", 
        goals="", 
        roles="", 
        personality="", 
        qualifications="", 
        elaboration="", 
        subtr="", 
        agent_type=""
        )
    WorldBuilding_agent = WorldBuildingAgent(
        name="", 
        goals="", 
        roles="", 
        personality="", 
        qualifications="", 
        elaboration="", 
        subtr="", 
        agent_type=""
        )
    WorldBuilding_agent = WorldBuildingAgent(
        name="", 
        goals="", 
        roles="", 
        personality="", 
        qualifications="", 
        elaboration="", 
        subtr="", 
        agent_type=""
        )
    WorldBuilding_agent = WorldBuildingAgent(
        name="", 
        goals="", 
        roles="", 
        personality="", 
        qualifications="", 
        elaboration="", 
        subtr="", 
        agent_type=""
        )
    
    instances = get_instances_of_subclasses(Agent)
    for instance in instances:
        instance.say_hello()
