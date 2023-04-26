from .apis import *
from .agent_utils import *
from pprint import pprint
from termcolor import colored

class AbstractEngine():
    ai_api = OpenAiAPI()
    agent = {}
    awareness = 'as_bot'
    expose_rest = True
    project = {}
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
    
    def submit_chat_prompt(self, prompt, prompting_agent, responding_agent):
        print(colored("AbstractEngine.submit_chat_prompt(): Submitting chat prompt...", "green"))
        request_data = self.open_ai_chat_data
        request_data['content'] = prompt
        request_data['prompting_agent'] = prompting_agent
        request_data['responding_agent'] = responding_agent
        response = self.ai_api.gpt_chat_response(request_data)
        print(colored("AbstractEngine.submit_chat_prompt(): Chat prompt submitted.\n\n", "green"))
        return prompt, response
        
    def start_engine(self):
        return self.wake_up()
    
    def wake_up(self):
        capability_id=0
        print(colored(f"AbstractEngine.wake_up(): Starting engine for {self.name}...", "green"))
        prompt = Prompt().to_wake_up(self)
        prompt, response = self.submit_chat_prompt(prompt, get_user_agent_singleton(), self)
        self.awake = True
        self.most_recent_responses_to['start_engine'] = response
        print(colored(f"AbstractEngine.wake_up(): {self.name} engine started.", "green"))
        self.save()
        return prompt, response

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
        print(colored("AbstractEngine.thoughts_concerns_propose_next_steps(): Sharing thoughts, concerns, and proposed next steps...", "green"))
        request_data = self.open_ai_chat_data
        request_data['content'] = Prompt().thoughts_concerns_proposed_next_steps(self, agent_to_share_with)
        response = self.submit_chat_prompt(self, request_data['content'], agent_to_share_with)
        self.most_recent_responses_to['thoughts_concerns_proposed_next_steps'] = response
        print(colored("AbstractEngine.thoughts_concerns_propose_next_steps(): Thoughts, concerns, and proposed next steps shared.", "green"))
        return request_data['content'], response

    def submit_state_report_to(self, agent):
        capability_id=7
        print(colored("AbstractEngine.submit_state_report_to(): Submitting report...", "green"))
        request_data = self.open_ai_chat_data
        report = self.report()
        request_data['content'] = self.compress_prompt(self, report, agent)
        response = self.submit_chat_prompt(self, request_data['content'], agent)
        self.most_recent_responses_to['report_to'] = response
        print(colored("AbstractEngine.submit_state_report_to(): Report submitted.", "green"))
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
        print(colored("AbstractEngine.report(): Generating report...", "green"))
        report = {}
        if self.awake:
            report = {
                "report_from": self.report_from(),
                "awake": True,
                "report":{
                    "conext":{
                        "recent_script_entries": self.script_for.recent_script_entries(),
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
        print(colored("AbstractEngine.report(): Report generated.", "green"))
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
    
    def compress(self, text_to_compress, compression_ratio=0.5):
        capability_id=18
        request_data = self.open_ai_chat_data
        prompt = Prompt().to_compress(text_to_compress, compression_ratio)
        print(colored("CompressionAgentEngine.compress_prompt(): Compressing prompt...", "green"))
        p, response = self.submit_chat_prompt(prompt, get_user_agent_singleton(), self)
        return response
   
 
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
        prompt = Prompt().to_assess(
            self, {
                "project": project, 
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
        print(colored("OrchestrationEnginne.amend_project(): Amending project...", "green"))
        response = self.ai_api.submit_chat_prompt(self, compressed_prompt, get_user_agent_singleton())
        self.most_recent_responses_to['amend_project'] = response
        return compressed_prompt, response
          
    def resume_project(self):
        capability_id=103
        print(colored("OrchestrationEnginne.resume_project(): Resuming project...", "green"))
        #for now, just print the data so we can assess it!
        print(colored(f"OrchestrationEnginne.resume_project(): {self.most_recent_responses_to['amend_project']})", 'green'))

    def provide_orchestrators_report_to_user():
        pass
    
    def establish_project_objective(self, project):
        print(colored(f"OrchestrationEnginne.establish_project_objective(): {self}", "green"))
        prompt = Prompt().to_establish_project_objective(project, self)
        objectives_prompt, objectives_response = self.submit_chat_prompt(prompt, get_user_agent_singleton, self)
        return objectives_response
    
    def assess_project_state(self, project):
        print(colored(f"OrchestrationEnginne.assess_project_state(): {self}", "green"))
        prompt = Prompt().to_assess_project_state(project, self)
        project_state_prompt, project_state_response = self.submit_chat_prompt(prompt, get_user_agent_singleton, self)
        return project_state_response
    
    def crud_agents_to_parts_of_project(self, project):
        print(colored(f"OrchestrationEnginne.crud_agents_to_parts_of_project(): {self}", "green"))
        pass
    
    def routine(self, project):
        #establish goals of the project
        if project.orc_agent_set_objectives == '': 
            project.orc_agent_set_objectives = self.establish_project_objective(project)
            print(colored(f"OrchestrationEnginne.routine(): Project objectives set by Orchestrator {project.orc_agent_set_objectives}", "green"))
        else:
            #reassess project objectives
            pass    
        project_state_assessment_response = self.assess_project_state(project)
        print(colored(f"OrchestrationEnginne.routine(): Project state assessment by Orchestrator {project_state_assessment_response}", "green"))
        user_input = input("hit enter to continue...")
        # self.crud_agents_to_parts_of_project(project, project_state_response)
        # self.run_agents(project)
        # self.assess_agent_output(project)
        # self.commit_agent_output_to_project(project)
        
    