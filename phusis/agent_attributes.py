
import uuid
from django.db import models
from django.apps import apps
from termcolor import colored
from pprint import pprint

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
    
    def to_dict(self):
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
    agent_attribute_type = 'orchestration_agent_goal'

class AgentRole(AbstractAgentAttribute):
    agent_attribute_type = 'agent_role'

class OrcAgentRole(AgentRole):
    agent_attribute_type = 'orchestration_agent_role'

class AgentPersonalityTrait(AbstractAgentAttribute):
    agent_attribute_type = 'agent_personality_trait'

class OrcAgentPersonalityTrait(AgentPersonalityTrait):
    agent_attribute_type = 'orchestration_agent_personality_trait'

class AgentQualification(AbstractAgentAttribute):
    agent_attribute_type = 'agent_qualification'

class OrcAgentQualification(AgentQualification):
    agent_attribute_type = 'orchestration_agent_qualification'

class AgentImpersonation(AbstractAgentAttribute):
    agent_attribute_type = 'agent_impersonation'

class OrcAgentImpersonation(AgentImpersonation):
    agent_attribute_type = 'orchestration_agent_impersonation'

class AgentStrength(AbstractAgentAttribute):
    agent_attribute_type = 'agent_strength'

class OrcAgentStrength(AgentStrength):
    agent_attribute_type = 'orchestration_agent_strength'

class AgentLocation(AbstractAgentAttribute):
    agent_attribute_type = 'agent_location'

class OrcAgentLocation(AgentLocation):
    agent_attribute_type = 'orchestration_agent_location'

class AgentDrive(AbstractAgentAttribute):
    agent_attribute_type = 'agent_drive'

class OrcAgentDrive(AgentDrive):
    agent_attribute_type = 'orchestration_agent_drive'

class AgentFear(AbstractAgentAttribute):
    agent_attribute_type = 'agent_fear'

class OrcAgentFear(AgentFear):
    agent_attribute_type = 'orchestration_agent_fear'

class AgentBelief(AbstractAgentAttribute):
    agent_attribute_type = 'agent_belief'

class OrcAgentBelief(AgentBelief):
    agent_attribute_type = 'orchestration_agent_belief'

class AgentAttitude(AbstractAgentAttribute):
    agent_attribute_type = 'agent_belief'

class OrcAgentAttitude(AgentAttitude):
    agent_attribute_type = 'orchestration_agent_attitude'

class AgentFavoredTheme(AbstractAgentAttribute):
    agent_attribute_type = 'agent_favored_theme'
 
class OrcAgentFavoredTheme(AgentFavoredTheme):
    agent_attribute_type = 'orchestration_agent_favored_theme'

class AgentFavoredGenre(AbstractAgentAttribute):
   agent_attribute_type = 'agent_favored_genre'
        
class AgentFavoredGenreCombo(AbstractAgentAttribute):
    agent_attribute_type = 'agent_favored_genre_combo'        
        
class AgentInspirationalSource(AbstractAgentAttribute):
    agent_attribute_type = 'agent_inspirational_sources'         

class AgentWritingStyle(AbstractAgentAttribute):
    agent_attribute_type = 'agent_writing_style'
        
class AgentCreatedTrait(AbstractAgentAttribute):
    agent_attribute_type = 'agent_created_trait'
    agent_created_trait_field = models.CharField(max_length=200, null=True, unique=True, default='')
    agent_created_trait_values = models.JSONField(null=True, blank=True, default=list)
    
    def set_data(self, properties_json):
        # pprint(properties_json)
        # print(properties_json.get('trait_field'))
        # print(properties_json.get('trait_value'))
        self.agent_created_trait_field = properties_json.get('trait_field', self.agent_created_trait_field)
        self.agent_created_trait_values.append(properties_json.get('trait_value'))
        self.elaboration = properties_json.get('elaboration', self.elaboration)
        self.name = f"Agent Created Trait: {self.agent_created_trait_field}"
        self.save()

class OrcAgentCreatedTrait(AgentCreatedTrait):
    agent_attribute_type = 'orchestration_agent_created_trait'


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
                # print(colored(f"find_agent_attribute_by(): FOUND: {attribute_class}, {instance}", "green"))            
                return attribute_class, instance
           
    # print(colored(f"find_agent_attribute_by(): NOT FOUND: {attribute_class}, {attribute_name}", "yellow"))
    
    data = {
        "class_name": attribute_class.__name__,
        "properties":{
            "name": attribute_name
        }
    }

    return attribute_class, load_or_get_agent_attribute_from(data)


def is_valid_init_json(json_data):
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
    
    if is_valid_init_json(json_data):
        attribute_class = apps.get_model("phusis", f"{json_data['class_name']}")
        if json_data['class_name'] == "AgentCreatedTrait" or json_data['class_name'] == "OrcAgentCreatedTrait":
            # pprint(json_data)
            new_attribute_obj, created = attribute_class.objects.update_or_create(
                name=f"Agent Created Trait: {json_data['properties']['trait_field']}",
                defaults={
                    'agent_created_trait_field': json_data['properties']['trait_field'],
                    'agent_created_trait_values': json_data['properties']['trait_values']
                }
            )
            return new_attribute_obj
        else:        
            # print(colored(f"load_or_get_agent_attributefrom(): Loading {json_data['properties']['name']}", "green"))
            new_attribute_obj, created = attribute_class.objects.get_or_create(name=json_data['properties']['name'])
            
            new_attribute_obj.set_data(json_data['properties'])
            
            s = "found and updated"
            if created: s = "created"
            # print(colored(f"load_agent_attributes_from(): {new_attribute_obj.name} {s}", "green")) 
        
        # new_attribute_obj.save()
    else:
        print(colored(f"models.load_agent_attributes_from: JSON data for att not valid, expected schema below","red"))
        print(colored(f"Data received: {json_data}", "red"))
        print(colored(f"Minimum expected: {expected_json}", "yellow"))   
    
    return new_attribute_obj        
    
    