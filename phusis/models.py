import inspect, json, uuid
from django.db import models
from noveller.models import *
from pprint import pprint

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200)
    agents = models.ManyToManyField('Agent')
    swarm_goals = models.ManyToManyField('AgentGoal')

    def __str__(self):
        return self.name

class AbstractAgent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, default="")
    agent_type = models.CharField(max_length=200, default="", editable=False)
    goals = models.ManyToManyField('AgentGoal', blank=True)
    roles = models.ManyToManyField('AgentRole', blank=True)
    personality = models.ManyToManyField('AgentTrait', blank=True)
    qualifications = models.ManyToManyField('AgentQualification', blank=True)
    subtr = models.TextField(blank=True)
    elaboration = models.TextField(blank=True)
    
    # concerned_with = models.ManyToManyField()
    
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
            "subtr": self.subtr,
            "elaboration": self.elaboration
        }
        
    def introduction(self):
        dict_str = json.dumps(self.dictionary(), indent=4)
        
        return f"Hi! I am an instance of the {self.agent_type} type of AI agent.\nHere are my basic attributes:\n{dict_str}"

class OrchestrationAgent(AbstractAgent):
    agent_type = "orchestration_agent"
    
class PoeticsAgent(AbstractAgent):
    agent_type = "poetics_agent"
    
class StructuralAgent(AbstractAgent):
    agent_type = "structural_agent"
     
class CharacterAgent(AbstractAgent):
    agent_type = "character_agent"
    
class ResearchAgent(AbstractAgent):
    agent_type = "research_agent"
    
class WorldBuildingAgent(AbstractAgent):
    agent_type = "world_building_agent"
    
class ThemeExploringAgent(AbstractAgent):
    agent_type = "theme_exploring_agent"
    
class ConflictAndResolutionAgent(AbstractAgent):
    agent_type = "conflict_and_resolution_agent"
    
class InterdisciplinaryAgent(AbstractAgent):
    agent_type = "interdisciplinary_agent"
    
class QualityEvaluationAgent(AbstractAgent):
    agent_type = "qualitye_valuation_agent"
        
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


def get_instances_of_subclasses_of(base_class):
    # Get all subclasses of the given base class
    subclasses = []
    for subclass in base_class.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_instances_of_subclasses_of(subclass))
        
    # Create a new list of instances
    instances = []
    for subclass in subclasses:
        instances.extend(list(subclass.objects.all()))
        
    for instance in instances:
        instance.subclass = subclass
    
    return instances

#testing
from django.db import transaction

def test_from_manager():
    with transaction.atomic():
        test_name_appendage = '_tst'
        
        agent = OrchestrationAgent.objects.create(name="Agent1")
        agent.save(using='default')
        
        agent_goal = AgentGoal.objects.create(name="My Goal1", elaboration="Description of my goal1.")
        agent_goal.save(using='default')
        agent_Role1 = AgentRole.objects.create(name="My Role1", elaboration="Description of my role1.")
        agent_Role1.save(using='default')
        agent_Role2 = AgentRole.objects.create(name="My Role2", elaboration="Description of my role2.")
        agent_Role2.save(using='default')
        agent_Role3 = AgentRole.objects.create(name="My Role3", elaboration="Description of my role3.")
        agent_Role3.save(using='default')
        agent_trait = AgentTrait.objects.create(name="My Trait1", elaboration="Description of my trait1.")
        agent_trait.save(using='default')
        agent_qualiificaton = AgentQualification.objects.create(name="My qualification1", elaboration="Description of my qualification1.")
        agent_qualiificaton.save(using='default')
        
        agent.goals.set([agent_goal])
        agent.roles.set([agent_Role1, agent_Role2, agent_Role3])
        agent.personality.set([agent_trait])
        agent.qualifications.add(agent_qualiificaton)
        
        listOfAttributes = [
            agent_goal,
            agent_Role1,
            agent_Role2,
            agent_Role3,
            agent_trait,
            agent_qualiificaton
        ]
            
        for att in listOfAttributes:
            att.name = f"{att.name}{test_name_appendage}"
            att.save(using='default')
            
        listOfAgents = [
            agent,
            CompressionAgent.objects.create(
                name="tightest of the compressors", 
                elaboration="Elaboration", 
                subtr="don't look so closley"
            ),
            InterdisciplinaryAgent.objects.create(
                name="Philosopher of alien violence", 
                elaboration="Elaboration", 
                subtr="don't look inside"
                ),
            WorldBuildingAgent.objects.create(
                name="Alien world builder", 
                elaboration="Elaboration", 
                subtr="don't look up"
                ),
            WorldBuildingAgent.objects.create(
                name="Earth 2.0 World Builder", 
                elaboration="Elaboration", 
                subtr="don't look beyond"
                ),
            WorldBuildingAgent.objects.create(
                name="Builder of underwater worlds", 
                elaboration="Elaboration", 
                subtr="don't look below"
                )
        ]
        
        for agent in listOfAgents:
            agent.goals.set([agent_goal])
            agent.roles.set([agent_Role1,agent_Role2,agent_Role3])
            agent.personality.set([agent_trait])
            agent.qualifications.set([agent_qualiificaton])
            agent.name = f"{agent.name}_tst"
            agent.save(using='default')
        
        print('geting instances agents')
        agent_instances = get_instances_of_subclasses_of(AbstractAgent)
        for instance in agent_instances:
            print("---------------------")
            print(instance.introduction())
            
        print('geting instances agent attributes')
        agent_att_instances = get_instances_of_subclasses_of(AbstractAgentAttribute)
        for instance in agent_att_instances:
            print("---------------------")
            print(json.dumps(instance.dictionary(), indent=4))
        
        print('deleting instances of agents')
        for instance in agent_instances:
            type(instance).objects.filter(name__contains=test_name_appendage).delete()
            
        print('deleting instances of agent attributes') 
        for instance in agent_att_instances:
            print(f"{type(instance)}.objects.filter(name='_tst').delete()")
            type(instance).objects.filter(name__contains=test_name_appendage).delete()
        
        print(f'confirming no {test_name_appendage} agent attributes are left')
        agent_att_instances = get_instances_of_subclasses_of(AbstractAgentAttribute)
        for instance in agent_att_instances:
            if({test_name_appendage} in instance.name):
                print("---------------------")
                print(instance.introduction())
            
        print(f'confirming no {test_name_appendage} agents are left')
        agent_instances = get_instances_of_subclasses_of(AbstractAgent)
        for instance in agent_instances:
            if({test_name_appendage} in instance.name):
                print("---------------------")
                print(json.dumps(instance.dictionary(), indent=4))
