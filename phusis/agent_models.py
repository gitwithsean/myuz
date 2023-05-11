import uuid, os
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .apis import *
from termcolor import colored
from django.db import models
from abc import abstractmethod
from .agent_attributes import *
from .agent_engines import *
from .agent_memory import ProjectMemory
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



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
        
        if self.compressed_prompt_content == '' and self.prompt: self.compressed_prompt_content = compress_text(self.prompt, 0.75)
        if not self.compressed_response_content == '' and self.response: self.compressed_response_content = compress_text(self.response, 0.75)
        self.save()
        prompt_obj = {"role": "user", "content": f"{self.compressed_prompt_content}"}
        response_obj = {"role": "assistant", "content": f"{self.compressed_response_content}"}
        # return [prompt_obj, response_obj]
        return [prompt_obj]
  
        
class AgentAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    assignment_str = models.TextField(blank=True, null=True, default='')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.UUIDField(blank=True, null=True)
    assignment_proj_att = GenericForeignKey('content_type', 'object_id')
    additional_assignment_instructions = models.TextField(blank=True, null=True, default='')
    related_project_goal_steps = models.ManyToManyField('PhusisProjectGoalStep', related_name='project_goal_steps_for_agent_assignment', blank=True, default=list)
    agent_for_assignment = models.ForeignKey('AbstractAgent', related_name='agent_for_assignment', on_delete=models.CASCADE, blank=True, null=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "agent_assigned" : {
                "agent_id" : str(self.agent_for_assignment.id),
                "agent_type" : self.agent_for_assignment.agent_type,
                "agent_name" : self.agent_for_assignment.agent_name,
            },
            "assignment" :{                
                "assignment_proj_att" : self.assignment_proj_att.name,
                "assignment_str" : self.assignment_str
            }
        }
    
    
class PhusisProjectGoalStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=1000, blank=False, null=False)
    related_project_attributes = models.ManyToManyField('ConcretePhusisProjectAttribute', related_name='project_attributes_for_project_goal_step', blank=True, default=[])
    
    def __str__(self):
        return f"{self.name}"
    
    def add_agent_assignment_to_step(self, assignment_obj):
        agent_name = assignment_obj['agent_assigned']['agent_name']
        agent = AbstractAgent.objects.get(name=agent_name)
        new_assignment = AgentAssignment(agent_assigned=agent)
        
        if assignment_obj['assignment']['assignment_str']:
            new_assignment.assignment_str = assignment_obj['assignment']['assignment_str']
        
        if assignment_obj['assignment']['assignment_proj_att']:    
            new_assignment.assignment_proj_att = AbstractPhusisProjectAttribute.objects.get(name=assignment_obj['assignment']['assignment_proj_att'])
        
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
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "related_project_attributes": [att.to_dict() for att in self.related_project_attributes.all()]
        }
   
       
class PhusisProjectGoal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=1000, blank=False, null=False, default='')
    steps = models.ManyToManyField('PhusisProjectGoalStep', blank=True, default=[])

    def __str__(self):
        return f"{self.name}"

    def add_steps_to_goal(self, steps):
        print(colored(f"PhusisProjectGoal.add_steps_to_goal:\n   goal_name: {self.name}\n   steps_for_goal:\n{steps}", "yellow"))
        
        for step in steps:
            new_step = PhusisProjectGoalStep(name=step)
            self.save()
            new_step.save()
            self.steps.add(new_step)
            self.save()

    def steps_for_goal_to_str(self):
        steps = ""
        i = 0
        for step in self.steps.all():
            i += 1
            steps += f"Step {i}: {step.name}\n"
            if step.related_project_attributes.exists():
                steps += f"- related attributes: {step.related_project_attributes.all()}\n"
        
        return steps

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "steps": [step.to_dict() for step in self.steps.all()]
        }

class AbstractPhusisProjectAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.content_type_id:  # Use self.content_type_id instead of self.content_type
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super().save(*args, **kwargs)
    
    
    def get_brief(self):
        return f"{self.name}"
               
    class Meta:
        abstract = True
        unique_together = ('name', 'content_type')

  
   
class ConcretePhusisProjectAttribute(AbstractPhusisProjectAttribute):
    class Meta:
        abstract = False   
   


class AbstractAgent(models.Model, AbstractEngine):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    agent_type = models.CharField(max_length=200, default="phusis_agent", editable=False)
    agent_system_prompt = models.TextField(blank=True)
    class_display_name = models.CharField(max_length=200, default='')
    # project_attributes_assigned_to = models.ManyToManyField('AbstractPhusisProjectAttribute', blank=True)
    # [{"prompted_by":"", "AgentCapability":{}, "result":""}]
    steps_taken = models.JSONField(default=list, blank=True)
    capabilities = models.ManyToManyField(AgentCapability, blank=True)
    embedding_of_self = models.TextField(blank=True)
    chat_logs = models.ManyToManyField(ChatLog, blank=True)
    awake = models.BooleanField(default=False)
    wake_up_message = models.TextField(blank=True, null=True)
    compressed_wake_up_message = models.TextField(blank=True, null=True)
    assignments_for_agent = models.ManyToManyField(AgentAssignment, blank=True, default=[], related_name='%(class)s_assigned_agents')
    phusis_applicaton = "noveller"
    
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

            # #Deal with capabilities first
            # if key == 'capabilities':
            #     self.capabilities.set(get_agent_capabilities_by_capability_ids()) 
                
            # Check if it's a ManyToManyField
            # elif isinstance(field, models.ManyToManyField):
            if isinstance(field, models.ManyToManyField):
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

    def goals_dict(self):
        goals_dict = []
        
        for goal in self.goals.all():
            goal_dict = goal.to_dict()
            goals_dict.append(goal_dict)
        
        return goals_dict


class OrchestrationAgent(AbstractAgent, OrchestrationEngine):
    class_display_name = "Orchestration Agent"
    agent_type = "orchestration_agent"
    # capabilities =  get_agent_capabilities_by_capability_ids([100,101,102,103])



class UserAgentSingleton(AbstractAgent):
    name = "user"
    agent_type = "user_agent"
    class_display_name = 'User'
    _instance = None
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



class AbstractPhusisProject(models.Model, ProjectMemory):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=500, default='', unique=True)
    project_type = models.CharField(max_length=200, default='Phusis Project')
    project_user_input = models.TextField(blank=True, default='')
    project_workspace = models.CharField(max_length=200, default='', blank=True, null=True)
    goals_for_project = models.ManyToManyField(PhusisProjectGoal, blank=True, default=[])
    agent_assignments_for_project = models.ManyToManyField(AgentAssignment, related_name='projects_for_agent_assignment', blank=True, default=list)   
    orchestrator = models.ForeignKey(OrchestrationAgent, related_name='orchestrator_for_project', on_delete=models.CASCADE, blank=True, null=True)
    project_embedding = models.TextField(blank=True)
    phusis_applicaton = models.CharField(max_length=200, default='', blank=False, null=False, auto_created=True, editable=False)
    project_attributes = models.ManyToManyField(AbstractPhusisProjectAttribute, related_name='attributes_for_project', blank=True, default=list)   
        
    def __str__(self):
        return f"{self.project_type}: {self.name}"

       
    class Meta:
        abstract = True
        ordering = ['name']
    
    
    def get_project_vector_metadata(self):
        return {
            "for_project": self.name,
            "for_project_type": self.project_type,
            "for_phusis_impl": self.phusis_applicaton,
        }
        
    def add_to_goals_for_project(self, goals):
        print(colored(f"AbstractPhusisProject.add_to_goals_for_project: project: {self.name} goals:\n{goals}", "yellow"))
        
        for goal in goals:
            new_goal = PhusisProjectGoal(name=goal)
            new_goal.save()
            self.save()
            self.goals_for_project.add(new_goal)
            self.save()

    def set_data(self, properties_dict):
        for key, value in properties_dict.items():
            attr_type = type(getattr(self, key))
            if attr_type == list:
                getattr(self, key).append(value)
            else:
                setattr(self, key, value)
        
        # self.project_workspace = get_phusis_project_workspace(self.project_type, self.name)

        self.save()
        
    def get_phusis_project_workspaces(self):
        INCOMING_FILES="/files_to_embed/"
        OUTGOING_FILES="/files_created/"
        LOGS="/logs/"
        myuz_dir = os.getcwd() 
        
        print(colored(f"agent_utils.get_phusis_project_workspace: myuz_dir set to {myuz_dir}", "yellow"))
        phusis_project_workspace = f"{myuz_dir}/{self.phusis_applicaton}/phusis-projects/{spaced_to_underscore(self.name)}"
        
        if self.project_workspace != "": 
            phusis_project_workspace = self.project_workspace
            
        workspaces = {
            "phusis_project_workspace" : phusis_project_workspace,
            "incoming_files" : f"{phusis_project_workspace}{INCOMING_FILES}",
            "outgoing_files" : f"{phusis_project_workspace}{OUTGOING_FILES}",
            "logs" : f"{phusis_project_workspace}{LOGS}"
        }  
        
        return workspaces   
    
    def goals_for_project_to_str(self):
        return [goal.name for goal in self.goals_for_project.all()]
     
    @abstractmethod
    def list_project_attributes(self):
        pass
    
    @abstractmethod
    def project_attributes(self):
        pass
    
    @abstractmethod
    def project_attributes_to_md(self):
       pass
    
    @abstractmethod
    def get_project_details(self, to='assess'):
        pass
    
    @abstractmethod
    def add_agents_to(self, agents):
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

 

# def load_agent_model_and_return_instance_from(json_data, app_name):
#     new_agent_obj = {}
#     expected_json = {
#         "class_name": "AgentsClassName",
#         "properties": {
#             "name": "Agent name"
#         }
#     }
 
#     if is_valid_init_json(json_data):
#         model_class = {}
#         if json_data['class_name'] in globals():
#             model_class = globals.get_model(app_name, f"{json_data['class_name']}")
#             print(colored(f"agent_models.load_agent_model_and_return_instance_from: model_class {model_class} found", "green"))
#         else: 
#             print(colored(f"agent_models.load_agent_model_and_return_instance_from: class_name {json_data['class_name']} not found in globals()", "red"))
#             pass
        
#         print(colored(f"agent_models.load_agent_model_and_return_instance_from: model_class: {model_class}", "yellow"))
#         print(colored(f"agent_models.load_agent_model_and_return_instance_from: json_data: {json_data}", "yellow"))
#         new_agent_obj, created = model_class.objects.update_or_create(name=json_data['properties']['name'])
        
#         new_agent_obj.set_data(json_data['properties'])
#         s = "found and updated"
#         if created: s = "created"
#         # print(colored(f"agent_models.load_agent_model_and_return_instance_from: {new_agent_obj.name} {s}", "green"))
        
#     else:
#         print(colored(f"agent_models.create_agent_model_from_instance: JSON data for agent not valid, expected schema below","red"))
#         print(colored(f"Data received: {json_data}", "red"))
#         print(colored(f"Minimum expected: {expected_json}", "yellow"))

#     return new_agent_obj


