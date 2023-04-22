import mimetypes, PyPDF2, sys, nltk, spacy, json
from .apis import *
from .agent_utils import *
from django.db import models
from datetime import datetime
from pprint import pprint
from django.contrib.postgres.fields import ArrayField

class PhusisScript():
    in_debug_mode = True
    script_content = ArrayField(models.JSONField(), default=list)
    class_display_name = 'Swarm Script'
    script_file_name = models.CharField(max_length=200, default="", editable=False)
    path_to_script = models.CharField(max_length=200, default="", editable=False)
    
    def __init__(self):
        self.path_to_script=f"{get_phusis_project_workspace(self.__class__.__name__, self.name)}{LOGS}"        
        self.script_file_name = self.script_file_name = f"{self.name}_script_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.json"
        self.script_content = []

    def script_to_text(self):
        txt = ""
        for entry in self.script_content:
            s = f"speaker_name: {entry.get('speaker_name', '')}\n"
            s = f"text: {entry.get('text', '')}\n\n"
            txt = f"{txt}\n\n{s}"
        return txt 

    def save_script_to_file(self):
        print(colored(f"Saving script to {self.path_to_script}{self.script_file_name}", "green"))

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
        self.script_content.append(prompt_and_response)  # Access the list stored in the ArrayField
        # script_content_list.append(prompt_and_response)  # Append the new entry to the list
        # self.script_content = script_content_list  # Assign the updated list back to the ArrayField
        self.save()
        if self.in_debug_mode:
            pprint(prompt_and_response)
            
    def recent_script_entries(self, num_entries=5):
        capability_id=15
        print(colored(f"Retrieving {num_entries} most recent prompt_and_response script entries...", "green"))
        i = 0
        recent_entries = []
        
        #if self.script-content is not emtpy
        if self.script_content:        
            script_content_list = self.script_content.all()  # Access the list stored in the ArrayField
            for script_entry in reversed(script_content_list):
                pprint(script_entry)
                recent_entries.append(script_entry)
                num_entries = num_entries - 1
                if num_entries == 0:
                    break
            return recent_entries
        else:
            return None



class AbstractEngine(PhusisScript):
    ai_api = OpenAi()
    agent = {}
    awareness = 'as_bot'
    expose_rest = True
    most_recent_responses_to = {
        "start_engine": "",
        "thoughts_concerns_proposed_next_steps": "",
        "submit_report": ""
    }
    open_ai_completions_data = {
        "role": "user",
        "model": "text-ada-001",
        "temperature": 0.2,
        "max_tokens": 300,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    open_ai_chat_data = {
       'model':"gpt-3.5-turbo",
       'max_tokens':1000
    }
    
    def submit_chat_prompt(self, prompt, prompting_agent):
        print(colored("Submitting chat prompt...", "green"))
        request_data = self.open_ai_chat_data
        request_data['content'] = PromptBuilderSingleton().complete_prompt(prompt, prompting_agent)
        response = self.ai_api.gpt_chat_response(request_data)
        print(colored("Chat prompt submitted.", "green"))
        return prompt, response
        
    def start_engine(self):
        return self.wake_up()
    
    def wake_up(self):
        capability_id=0
        print(colored(f"Starting engine for {self.name}...", "green"))
        request_data = self.open_ai_chat_data
        # print(colored(f"Request Data to wake up {self.name}...", "green"))
        # pprint(request_data)
        request_data['content'] = PromptBuilderSingleton().to_wake_up(self)
        # print(colored(f"Content to wake up {self.name}...", "green"))
        # print(request_data['content'])
        response = self.ai_api.gpt_chat_response(request_data)
        pprint(response)
        self.awake = True
        self.most_recent_responses_to['start_engine'] = response
        print(colored(f"{self.name} engine started.", "green"))
        self.save()
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
        request_data = self.open_ai_chat_data
        request_data['content'] = PromptBuilderSingleton().thoughts_concerns_proposed_next_steps(self, agent_to_share_with)
        response = self.submit_chat_prompt(self, request_data['content'], agent_to_share_with)
        self.most_recent_responses_to['thoughts_concerns_proposed_next_steps'] = response
        print(colored("Thoughts, concerns, and proposed next steps shared.", "green"))
        return request_data['content'], response

    def submit_state_report_to(self, agent):
        capability_id=7
        print(colored("Submitting report...", "green"))
        request_data = self.open_ai_chat_data
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
            "personality_traits": list(self.personality_traits.all().values_list('name', flat=True)),
            "qualificatons": list(self.qualifications.all().values_list('name', flat=True)),
            "impersonations": list(self.impersonations.all().values_list('name', flat=True)),
            # "self-summarization": (self.summarize_self(), ''),
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

 
class WritingAgentEngine(AbstractEngine):
    pass



class CompressionAgentEngine(AbstractEngine):
    open_ai_chat_data = {
        "role": "user",
        "content": "",
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 1000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    
    def compress_prompt(self, prompt, compression_ratio=0.5, prompting_agent=()):
        capability_id=18
        if prompting_agent == {}: prompting_agent = get_user_agent_singleton()
        request_data = self.open_ai_chat_data
        request_data['content'] = PromptBuilderSingleton().to_compress(prompt, compression_ratio)
        print(colored("Compressing prompt...", "green"))
        return self.submit_chat_prompt(prompt, prompting_agent)



class EmbeddingsAgentEngine(AbstractEngine):
    pinecone_api = PineconeApi()
    file_size_limit = 3     # in MB
    open_ai_chat_data = {
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
    



class WebSearchAgentEngine(AbstractEngine):
    gooogle_api = GoogleApi()
    def perform_google_search(self, query):
        #
        capability_id=19
        print(colored(f"WebSearchAgentEngine.perform_google_search(): Performing Google search for {query}", "green"))
        
        return self.gooogle_api.get_google_search_results(query)
    
     
 
class OrchestrationEngine(AbstractEngine):
    auto_mode = False
    open_ai_chat_data = {
       'model':"gpt-3.5-turbo",
       'max_tokens':1000
    }
    awareness = 'as_leader_of_ai_swarm'
    latest_swarm_reports = []
    swarm_produced_files = []
    
    def assess_project(self, project):
        capability_id=100
        print(colored("OrchestrationEngine.assess_project(): Producing Swarm data for assess_project()...", "green"))
        self.gather_swarm_reports(project)
        
        latest_swarm_reports = self.latest_swarm_reports
        swarm_produced_files = self.swarm_produced_files
        
        print(colored("OrchestrationEngine.assess_project(): Producing prompt for assess_project()...", "green"))
        #From that data, produce assessment prompt
        prompt = PromptBuilderSingleton().to_assess(
            self, {
                "project": project, 
                "script_entries": self.recent_script_entries(), 
                "swarm_reports": latest_swarm_reports, 
                "swarm_produced_files": swarm_produced_files
            }
        )
        compressed_prompt = get_compression_agent_singleton().compress_prompt(prompt, 0.5)
        
        print(colored("OrchestrationEngine.assess_project(): Submitting compressed assessment prompt to ai api...", "green"))
        assessment_prompt, assessment_response = self.submit_chat_prompt(compressed_prompt, get_user_agent_singleton())
        
        self.most_recent_responses_to['assess_project'] = assessment_response

        return assessment_prompt, assessment_response

    
    def gather_swarm_reports(self, project):
        capability_id=101
        global latest_swarm_reports
        print(colored("OrchestrationEngine.gather_swarm_report(): Assessing agent swarm...", "green"))

        ## get all the agents in the project
        project_agents = project.get_agents_for()
        
        ## Get a report from each agent
        for agent_instance in project_agents:
            
            print(colored(f"OrchestrationEngine.gather_swarm_report(): Getting report from agent: {agent_instance.name}", "green"))
            
            self.latest_swarm_reports.append(agent_instance.report_from())
            self.swarm_produced_files.append(agent_instance.files_produced)
            
            
        print(colored("OrchestrationEngine.gather_swarm_report(): Reports from swarm gathered", "green"))
        
    def amend_project(self, project_details):
        capability_id=102
        prompt = prompt + f"\n\nHere is your most recent assessment of the project:\n\n{self.most_recent_responses_to['assess_project']}"
        prompt = prompt + f"\n\nHere is a user created introduction to the project: {project_details}"
        prompt = prompt + "\n\nGiven your most recent assessment of the project above, what do you think, given your expertise as an orchestrations agent, we need to do next? You have a variety of options, including, but not limited to.\nRequesting to wake up an agent and tasking them\nGiving new tasks to already awake agents\nAsking the User for more input\nWhatever else it is you think we could be doing to further the project\n"
        
        prompt = prompt + f"And as a reminder, this is who you are:\n\n{self.original_data}"
        
        compressed_prompt = get_compression_agent_singleton().compress_prompt(prompt, 0.5)
        print(colored("Amending project...", "green"))
        response = self.ai_api.submit_chat_prompt(self, compressed_prompt, get_user_agent_singleton())
        self.most_recent_responses_to['amend_project'] = response
        return compressed_prompt, response
          
    def resume_project(self):
        capability_id=103
        print(colored("Resuming project...", "green"))
        #for now, just print the data so we can assess it!
        print(self.most_recent_responses_to['amend_project'])

    def provide_orchestrators_report_to_user():
        pass