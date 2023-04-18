import json, uuid, os, mimetypes, sys, PyPDF2, nltk, spacy
from django.db import models
from django.apps import apps
from .apis import *
from datetime import datetime
from termcolor import colored
from pprint import pprint
 
 
class AbstractPhusisProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)    
    class Meta:
        abstract = True
   
   
#SCRIPTS
class Script(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, default="") 
    is_master_script = models.BooleanField(default=False)
    in_debug_mode = True
    #script as list of tuples speaker/spoken 
    # [ { date_time, speaker_id, speaker_name, content } ]
    script_content = models.JSONField(default=list, blank=True)
    agent = {}
    expose_rest = True
    class_display_name = 'Script'
        
    def script_file_name(self, agent={}):
        if agent=={}:
            agent=self.agent
        else:
            self.agent = agent    
        self.name = f"{self.agent.name}_script_{datetime.utcnow().strftime('%Y%m%d_%H%M')}"
        return f"scripts/{self.agent_name}/{self.name}.json"

    def script_to_text(self):
        txt = ""
        for entry in self.script_content:
            s = f"speaker_name: {entry.get('speaker_name', '')}\n"
            s = f"text: {entry.get('text', '')}\n\n"
            txt = f"{txt}\n\n{s}"
        return txt 

    def save_script_to_file(self):
        print(colored("Saving script to file...", "green"))
        os.makedirs(os.path.dirname(self.script_file_name()), exist_ok=True)
        with open(self.script_file_name(), "w") as f:
            json.dump({"script": {"script_entries": self.script_content}}, f, indent=4) 
        
    def add_script_entry(self, prompter, prompt, responder, response):
        capability_id=13
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
        self.script_content.append(prompt_and_response)
        self.save_script_to_file()
        if self.in_debug_mode:
            pprint(prompt_and_response)
            
    def recent_script_entries(self, num_entries=5):
        capability_id=14
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


#VECTORS
class Vector(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    content = models.TextField(blank=False)
    embeddings = models.TextField(blank=False)
    
    def is_file(self):
        return os.path.isfile(self.data)


#ABSTRACTS
class AbstractEngine():
    ai_api = OpenAi()
    agent = {}
    awareness = 'as_ai'
    awake = False
    expose_rest = True
    most_recent_responses_to = {
        "start_engine": "",
        "thoughts_concerns_proposed_next_steps": "",
        "submit_report": ""
    }
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
        print(colored("Engine started.", "green"))

    def consider(self, objs=[], prompt_adj=''):
        capability_id=1
        pass

    def produce(self, objs=[], prompt_adj=''):
        capability_id=2
        pass

    def reflect_on(self, objs=[], prompt_adj=''):
        capability_id=3
        pass
    
    def question_critisize(self, objs=[], prompt_adj=''):
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
        exec=8
        pass

    def return_production_content(self):
        exec=9
        pass

    def executive_summary_of(self, obj=[]):
        exec=10
        if obj.len()==0: obj.append(self)
        pass
    
    def delve(self):
        exec=11
        pass
    
    def improvise_on(self, obj=[]):
        exec=12
        if obj.len()==0: obj.append(self)
        pass
    
    def dwell_on(self, obj=[]):
        exec=13
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


class AbstractAgent(models.Model, AbstractEngine):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, default="")
    agent_type = models.CharField(max_length=200, default="phusis_agent", editable=False)
    class_display_name = models.CharField(max_length=200, editable=False, default=f"Phusis {agent_type} Agent")
    goals = models.ManyToManyField('AgentGoal', blank=True)
    roles = models.ManyToManyField('AgentRole', blank=True)
    personality_traits = models.ManyToManyField('AgentTrait', blank=True)
    qualifications = models.ManyToManyField('AgentQualification', blank=True)
    impersonations = models.ManyToManyField('AgentImpersonation', blank=True)
    is_concerned_with =  models.ForeignKey('noveller.ConcreteNovellerModelDecorator', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_concerned_with_this')
    is_influenced_by =  models.ForeignKey('noveller.ConcreteNovellerModelDecorator', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_influenced_by_this')
    embedding_of_self = models.TextField(blank=True)
    elaboration = models.TextField(blank=True)
    llelle = models.TextField(blank=True)
    malig = models.TextField(blank=True)
    subtr = models.TextField(blank=True)  
    script = models.OneToOneField('Script', null=True, blank=True, on_delete=models.PROTECT)
    capabilities = models.ManyToManyField('AgentCapability', blank=True)
    # {"prompted_by", "AgentCapability", "result"}
    steps_taken = models.JSONField(default=list, blank=True)
    expose_rest = True
    agent_created_traits = models.JSONField(default=list, blank=True)
    
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
        
    def introduce_yourself(self, is_brief=True):
        dict_str = json.dumps(self.dictionary(), indent=4)
        
        return f"Hi! I am an instance of the {self.agent_type} type of AI agent.\nHere are my basic attributes:\n{dict_str}"
 
 
class ConcreteAgent(AbstractAgent):
    is_concerned_with = models.ForeignKey('noveller.ConcreteNovellerModelDecorator', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)sagents_concerned_with_this')
    is_influenced_by = models.ForeignKey('noveller.ConcreteNovellerModelDecorator', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)sagents_influenced_by_this')
    
    class_display_name = "Concrete Agent (you shouldn't be seeing this)"
    script = models.OneToOneField('Script', editable=False, on_delete=models.PROTECT, related_name='concrete_agent_for_script', null=True, blank=True,)
    expose_rest = False
    
    class Meta:
        db_table = 'phusis_concrete_agent'
       
        
#ENGINES AND AGENTS
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
        
        compressed_prompt = CompressionAgent().compress_prompt(prompt, 0.7)
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
        
        compressed_prompt = CompressionAgent.compress_prompt(prompt, 0.5)
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
    #OBJECTIVE ORIENTED TRAITS
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    class_display_name = "Orchestration Agent"
    # name = models.CharField(max_length=200, default="")
    agent_type = "orchestration_agent"
    # original_data = {}
    goals = models.ManyToManyField('OrcAgentGoal', blank=True)
    roles = models.ManyToManyField('OrcAgentRole', blank=True)
    qualifications = models.ManyToManyField('OrcAgentQualification', blank=True)
    elaboration = models.TextField(blank=True)
    # script = models.OneToOneField('Script', null=True, blank=True, on_delete=models.PROTECT)
    
    #CHARACTER_TRAITS
    orc_character_age = models.IntegerField(null=True)
    orc_character_possible_locations = models.JSONField(default=list, blank=True)
    orc_character_personality_traits = models.ManyToManyField('OrcAgentTrait', blank=True, related_name='orc_character_personality_traits')
    orc_character_impersonations = models.ManyToManyField('OrcAgentImpersonation', blank=True, related_name='orc_character_impersonations')
    orc_character_attitudes = models.JSONField(default=list, blank=True)
    orc_character_strengths = models.JSONField(default=list, blank=True)
    orc_character_drives = models.JSONField(default=list, blank=True)
    orc_character_fears = models.JSONField(default=list, blank=True)
    orc_character_beliefs = models.JSONField(default=list, blank=True)
    orc_character_origin_story = models.TextField(blank=True)
    orc_character_llelle = models.TextField(blank=True)
    orc_character_malig = models.TextField(blank=True)
    orc_character_subtr = models.TextField(blank=True)
    expose_rest = True
    
    def __str__(self):
        return self.name
    
    def introduction(self):
        return AbstractAgent.introduce_yourself(self)
    
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
        if prompting_agent == {}: prompting_agent = UserAgentSingleton()
        request_data = self.open_ai_data
        request_data['content'] = PromptBuilderSingleton().to_compress(prompt, compression_ratio)
        print(colored("Compressing prompt...", "green"))
        return self.submit_chat_prompt(prompt, prompting_agent)


class CompressionAgent(AbstractAgent, CompressionAgentEngine):
    agent_type = "compression_agent"
    class_display_name = "Compression Agent"
    expose_rest = False


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
            ERROR in EmbeddingAgentEngine.create_embedding_for()
            Incorrect input type for function create_embedding_for
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
    
#Singleton    
class EmbeddingsAgentSingleton(AbstractAgent, EmbeddingsAgentEngine):
    name = "Embeddings Agent"
    agent_type = "embeddings_agent"
    class_display_name = "Embeddings Agent"
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


class StructuralAgent(AbstractAgent):
    # story plotting
    # story structure (r.g. experimental and/or tried and tested structures)
    # fleshing out the story structure and plotting based on the inputs from other agents in the swarm  
    agent_type = "structural_agent"
    class_display_name = "Structural Agent"


class CharacterAgent(AbstractAgent):
    # agents that flesh out character profiles in various different genres, styles, target audience profiles, etc
    # also agents that become the character so that a user or other agents can talk to them, or to produce dialog
    agent_type = "character_agent"
    class_display_name = "Character Agent"

 
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


class AgentCreatedAgents(AbstractAgent):
    # If any of the 'manager' agents feels there is a class of agent missing that they need
    #A list of tuples: { trait_field, trait_valuess [] }
    agent_created_attributes = []
    class_display_name = "Agent Created Agent"
 
        
#UTILITY AGENTS  
class WebSearchAgent(AbstractAgent):
    agent_type = "web_search_agent"
    class_display_name = "Web Search Agent"


#AGENT ATTRIBUTES
class AbstractAgentAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, null=True)
    agent_attribute_type = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True)
    expose_rest = True
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


class AgentCapability(AbstractAgentAttribute):
    agent_attribute_type = "agent_executable" 
    capability_id = models.IntegerField(blank=False, null=False)
    prompt_adjst = models.TextField(blank=True, null=True)
    parameters = models.JSONField(blank=True, default=list)
    output_schema = models.TextField(blank=True, null=True)


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


class OrcAgentCapability(AgentCapability):
    agent_attribute_type = "orchestration_agent_capability" 


#singleton
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
        
        prompt = f"You are {agent.name}, {s}. You will use your skills to the BEST of your ability to serve me, the human user, I will tell you our objective soon, but first, about you. {self.to_remind(agent)}"

        return self.auto_reminder(prompt, agent)  
    
    def thoughts_concerns_proposed_next_steps(self, agent, agent_to_share_with):
        prompt = f"{agent_to_share_with}, {agent_to_share_with.agent_type} of the swarm you are a member of, has requested for you to report back. They want you to reflect on what you have done so far, and respond in the following format as concisely as possible:\n\nTHOUGHTS:\n\nCONCERNS\n\nWHAT YOU THINK YOUR NEXT STEPS SHOULD BE:\n\n"
        return self.auto_reminder(prompt, agent) 
    
    def to_remind(self, agent):      
        prompt = f"Here is your character description: {agent.dictionary()}"
        
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

