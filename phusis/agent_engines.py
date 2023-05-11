from .apis import *
from .phusis_utils import *
from .prompter import Prompter
from termcolor import colored
import tiktoken, json, datetime

class AbstractEngine():
    ai_api = OpenAiAPI()
    agent = {}
    awareness = 'as_bot'
    project = {}
    most_recent_responses_to = {
        "start_engine": ""
    }
    
    def submit_chat_prompt(self, prompt, prompting_agent, responding_agent):
        print(colored("AbstractEngine.submit_chat_Prompter(): Submitting chat prompt...", "green"))
        request_data = self.open_ai_chat_data
        request_data['content'] = prompt
        request_data['prompting_agent'] = prompting_agent
        request_data['responding_agent'] = responding_agent
        response = agent_chatterer(request_data)
        print(colored("AbstractEngine.submit_chat_Prompter(): Chat prompt submitted.\n\n", "green"))
        return prompt, response
        
    def start_engine(self):
        return self.wake_up()
    
    def wake_up(self):
        capability_id=0
        if not self.awake:
            request_data = self.open_ai_chat_data
            print(colored(f"AbstractEngine.wake_up(): Starting engine for {self.name}...", "green"))
            
            prompt = Prompter().to_wake_up(self)
            request_data['content'] = prompt
            request_data['prompting_agent'] = get_user_agent_singleton()
            request_data['responding_agent'] = self
                        
            #we actually don't need to submit the prompt to the API, because we already have the response ("I understand and I'm ready!")
            response = "I understand and I'm ready!"
            self.wake_up_message = prompt
            
            # print(colored(f"AbstractEngine.wake_up(): right before compression, prompt is {prompt}", "yellow"))
            
            self.compressed_wake_up_message = compress_text(prompt, 0.75)
            self.awake = True           
            
            self.most_recent_responses_to['start_engine'] = response
            
            print(colored(f"AbstractEngine.wake_up(): {self.name} engine started.", "green"))
            
            self.save()
            
            return prompt, response
        return "already awake", "already awake"

class OrchestrationEngine(AbstractEngine):
    auto_mode = False
    open_ai_chat_data = {
       'model' : "gpt-4",
       'max_tokens' : 6000
    }
    array_of_project_goals = []
    awareness = 'as_orc'
    latest_swarm_reports = []
    swarm_produced_files = []
            
    def establish_project_goals(self, project):
        """
        Establish the goals for a given project by submitting a chat prompt.
        :param project: The project for which to establish goals.
        :return: The goals response.
        """
        print(colored(f"OrchestrationEngine.establish_project_goals():", "yellow"))
        prompt = Prompter().to_establish_project_goals(project, self)
        goals_prompt, goals_response = self.submit_chat_prompt(prompt, get_user_agent_singleton, self)
        return goals_response
    
    
    def set_sub_tasks_for_goal(self, goal):
        """
        Set subtasks for a given goal by submitting a chat prompt.
        :param goal: The goal for which to set subtasks.
        :return: The project state response.
        """        
        print(colored(f"OrchestrationEngine.set_sub_tasks_for_goal(): {goal}", "yellow"))
        prompt = Prompter().to_set_steps_for_project_goal(goal, self.project, self)
        project_state_prompt, project_state_response = self.submit_chat_prompt(prompt, get_user_agent_singleton, self)
        return project_state_response
    
    
    def assign_project_attributes_to_step(self, step, goal):
        """
        Assign project attributes to a given step by submitting a chat prompt.
        :param step: The step to assign project attributes to.
        :param goal: The goal associated with the step.
        :return: The attributes for step response.
        """
        print(colored(f"OrchestrationEngine.assign_project_attributes_to_step(): {step}", "yellow"))
        prompt = Prompter().to_assign_project_attributes_to_step(step, goal, self.project, self)
        atts_for_step_prompt, atts_for_step_response = self.submit_chat_prompt(prompt, get_user_agent_singleton, self)
        return atts_for_step_response
    
    
    def create_agent_assignments_for_step(self, step):
        """
        Create agent assignments for a given step by submitting a chat prompt.
        :param step: The step for which to create agent assignments.
        :return: The agent assignments response.
        """
        print(colored(f"OrchestrationEngine.create_agent_assignments_for_step(): {step}", "yellow"))
        prompt = Prompter().to_create_agent_assignments_for_step(step, self.project, self)
        agent_assignments_prompt, agent_assignments_response = self.submit_chat_prompt(prompt, get_user_agent_singleton, self)
        return agent_assignments_response 
        
        
    def routine(self, project):
        print(print(colored(f"\nOrchestrationEngine.routine(): Starting agent routine...\n", "green")))
        self.project = project
        
        print(colored(f"\nOrchestrationEngine.routine(): Project goals set by Orchestrator\n\n{project.goals_for_project}\n", "yellow"))
        
        goals_for_project = []
        
        #establish goals of the project
        if not project.goals_for_project.exists():
            print(colored(f"\nOrchestrationEngine.routine(): Project goals set by Orchestrator\n\n{project.goals_for_project}\n", "green"))   
            goals_for_project = json.loads(self.establish_project_goals(project))
            
            project.add_to_goals_for_project(goals_for_project)
            project.save()
               
        else:
            print(colored(f"\nOrchestrationEngine.routine(): Project goals already set by Orchestrator\n\n{project.goals_for_project}\n", "green"))
            #TODO re-assess goals?
        
        user_input = input("hit enter to continue...")
        
        print(colored(f"OrchestrationEngine.routine(): {project.goals_for_project_to_str()}", "green"))
        #establish steps for goals of the project
        for goal in project.goals_for_project.all():        
            if not goal.steps.exists():
                print(colored(f"\nOrchestrationEngine.routine(): Orchestrator now setting sub-tasks for project goal:\n{goal.name}\n", "yellow")) 
                #have orc create goals_for_project on the project object and assign them with substeps
                goal_steps = json.loads(self.set_sub_tasks_for_goal(goal))
                    
                goal.add_steps_to_goal(goal_steps)
                goal.save()
                project.save()
            else:
                print(colored(f"\nOrchestrationEngine.routine(): Orchestrator already set sub-tasks for this project goal {goal.name}\n\n{goal.steps}\n", "yellow"))
                #TODO re-assess steps in goal?

        user_input = input("hit enter to continue...")

        print(project.goals_for_project.all())
        #assign project attribute(s) to a step in a goal, if applicable
        for goal in project.goals_for_project.all():
            for step in goal.steps.all():
                if not step.related_project_attributes.exists():
                    print(colored("\nOrchestrationEngine.routine(): Orchestrator now assigning project attributes to each step in each project goal\n", "yellow"))
                    #have orc assign attribute(s) to the step
                    attributes_for_step = json.loads(self.assign_project_attributes_to_step(step, goal))
                    
                    step.add_project_attributes_to_step(attributes_for_step)
                else:
                    print(colored(f"\nOrchestrationEngine.routine(): Orchestrator already assigned project attributes to this step {step.name}\n\n{step.related_project_attributes}\n", "yellow"))
                    #re-assess attributes in step?
                    pass
        
        user_input = input("hit enter to continue...")       
        
        #create agent assignments for step in goals, if applicable
        for goal in project.goals_for_project.all():
            print(colored(f"agent_engines.routine(): goal {goal} has steps {goal.steps.all()}", "green"))
            for step in goal.steps.all():
                print(colored(f"\nOrchestrationEngine.routine(): {step.agent_assignments_for_step.all()}", "green"))
                if not step.agent_assignments_for_step.exists():
                    print(colored("\nOrchestrationEngine.routine(): Orchestrator now assigning agent(s) to step/attribute(s) for step\n", "yellow"))
                    #have orc create agent assignments for the step
                    agent_assignments_response = self.create_agent_assignments_for_step(step, goal)
                    
                    for assignment in agent_assignments_response:
                        if assignment['agent_assigned']['is_new']:
                            print(colored(f"\nOrchestrationEngine.routine(): Orchestrator now creating new agent {assignment['agent_assigned']['agent_name']} for {assignment}\n", "yellow"))
                            #TODO
                            pass
                    
                        project.agent_assignments_for_project.add(step.add_agent_assignment_to_step(assignment))
                    
                else:
                    print(colored(f"\nOrchestrationEngine.routine(): Orchestrator already assigned agent(s) to step/attribute(s) for step {step.name}\n\n{step.agent_assignments_for_step}\n", "yellow"))
                    #re-assess agent_assignments in step?
                    pass
        
        user_input = input("hit enter to continue...")
        
        #execute agent assignments for project
        for assignment in project.agent_assignments_for_project.all():
            print(colored(f"\nOrchestrationEngine.routine():Now running each agent assignment {assignment.agent_assigned.agent_name} for {assignment}\n", "yellow"))
            #TODO
            pass
        
        #allow agent_assignments to ask questions of other agent_assignments
        
        print(project.project_brief())
            
        # else:
        #     #reassess project goals?
        #     pass
        
        # #assign agents to a step in a goal 
        # for goal in self.array_of_project_goals:
        #     self.assign_agent_to_goal(goal)
        
        # project_state_assessment_response = self.assess_project_state(project)
        # print(colored(f"\nOrchestrationEngine.routine(): Project state assessment by Orchestrator {project_state_assessment_response}\n", "green"))
        
        user_input = input("hit enter to continue...")
        # self.crud_agents_to_parts_of_project(project, project_state_response)
        # self.run_agents(project)
        # self.assess_agent_output(project)
        # self.commit_agent_output_to_project(project)


    
def compress_text(text_to_compress, compression_ratio=0.5, model="gpt-3.5-turbo"):    
    """
    Asl gpt-3.5-turbo to ompress the given text by a ratio of {compression_ratio}
    :param text_to_compress: The text to compress.
    :param compression_ratio: The desired compression ratio (default is 0.5).
    :return: The compressed text.
    """
    opeanai_api = OpenAiAPI()
    open_ai_chat_data = {
        "model": model,
    }
    
    # print(colored(f"agent_engines.compress_text(): Compressing text to a ratio <= {compression_ratio}. Text = \n\n{text_to_compress}\n\nCompression...", "yellow"))

    prompt = f"Re-write the following text so that it uses {compression_ratio} the number of GPT tokens, and so that another GPT agent will receive the same information as would be conveyed by the original text. Completely rearrange the structure and use any technique that would help you achieve a better outcome. Your output does not need to be human-readable, but it should be easy for another GPT instance to interpret. Here is the text:\n```\n\n{text_to_compress}\n\n```"
    
    # print(colored("agent_engines.compress_text(): Compressing prompt...", "yellow"))
    
    api_data = open_ai_chat_data
    
    with open("./.secrets/openai_api_key", 'r') as f:
        api_data['key'] = f.read()
        
    api_data['messages_to_submit'] = []
    api_data['messages_to_submit'].append({"role": "system", "content": "You are a GPT agent with the role of reducing the amount of GPT tokens required to convey the meaning of a text to another GPT agent."})
    api_data['messages_to_submit'].append({"role": "user", "content": prompt})
    
    print(colored(f"\nagent_engines.compress_text(): messages_to_submit = \n", "yellow"))
    
    for message in api_data['messages_to_submit']:
        print(colored(f"\nrole: {message['role']}\n{message['content']}\n--------------", "yellow"))
    
    print(colored(f"\nagent_engines.compress_text(): sumbitting messages to api \n", "yellow"))
    
    response = opeanai_api.chat_response(api_data)
    
    print(colored(f"\nagent_engines.compress_text(): response =\n {response.choices[0].message.content}\n", "green"))
    
    return response.choices[0].message.content     
   
   
def agent_chatterer(api_data):
    """
    Start/Continue a conversation with a phusis agent.
    :param api_data: Data required for the conversation with the AI agent.
    :return: The AI agent's response.
    
    api_data: {
        "repsonding_agent": <Agent object>,
        "system_message": <message to send to chat agent to define what/who it is>,
        "model": <openai model to use>,
    }
    
    """
    opeanai_api = OpenAiAPI()

    api_data['key_file'] = "./.secrets/openai_api_key"
    
    with open(api_data['key_file'], 'r') as f:
        api_data['key'] = f.read()

    system_message = ""
    if api_data.get('system_message') != None:
        system_message = api_data['system_message']
    elif api_data['responding_agent'].compressed_wake_up_message != '':
        system_message = f"You are {api_data['responding_agent'].name}. {api_data['responding_agent'].compressed_wake_up_message}"
    else: 
        api_data['responding_agent'].wake_up()
        system_message = api_data['responding_agent'].wake_up_message
        
    api_data['messages_to_submit'] = [{"role": "system", "content": system_message}]
    
    if api_data['responding_agent'] != "UtilityAgent":
        i = 3
        if api_data['responding_agent'].chat_logs.all() != [] :
            for chat_log in api_data['responding_agent'].chat_logs.all(): 
                #some way to count the tokens in the chat log and not add if it goes beyond a limit, but for now, just the last i (3)
                if i > 0:
                    for obj in chat_log.convert_log_to_chain_objects():
                        api_data['messages_to_submit'].append(obj)
                        i = i - 1
    
    api_data['messages_to_submit'].append({"role": "user", "content": api_data.get("content")})
    
    print(colored(f"\nagent_engines.agent_chatterer(): messages_to_submit = \n", "yellow"))
    
    for message in api_data['messages_to_submit']:
        print(colored(f"\nrole: {message['role']}\n{message['content']}\n--------------", "yellow"))
    
    print(colored(f"\nagent_engines.agent_chatterer(): sumbitting messages to api\n", "yellow"))
    
    response = opeanai_api.chat_response(api_data)
    
    print(colored(f"\nagent_engines.agent_chatterer(): response =\n{response.choices[0].message.content}\n", "green"))
    
    if api_data['responding_agent'].agent_type == "orchestration_agent":
        token_logging(response, './.secrets/orc_agent_token_usage.json')
    
    # token_logging(response, f"./.secrets/{api_data['model']}token_usage.json")
        
    return response.choices[0].message.content
       
       
def token_logging(response, json_file_path = './.secrets/orc_agent_token_usage.json'):
    """
    Log token usage for different kinds of agents (orc or otherwise).
    :param response: The API response containing token usage information.
    :param json_file_path: The path to the JSON file storing the daily token usage (default is './.secrets/orc_agent_token_usage.json').
    """
    
    today = datetime.date.today().strftime('%Y-%m-%d')

    new_completion_tokens = int(response['usage']['completion_tokens'])
    new_prompt_tokens = int(response['usage']['prompt_tokens'])

    # Load daily_token_usage from the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        daily_token_usage = data['daily_token_usage']

    # Check if today's entry exists
    today_entry = None
    for day in daily_token_usage:
        if day['date'] == today:
            today_entry = day
            break

    # If today's entry doesn't exist, create a new one and append it to daily_token_usage
    if today_entry is None:
        today_entry = {
            "date": today,
            "prompt_tokens": 0,
            "completion_tokens": 0
        }
        daily_token_usage.append(today_entry)

    # Update today's entry with the new tokens
    today_entry['completion_tokens'] += new_completion_tokens
    today_entry['prompt_tokens'] += new_prompt_tokens

    # Save the updated daily_token_usage to the JSON file
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)


# def parse_list_string_to_list(input_string):
#     """
#     Parse a string representing a list into a Python list.
#     :param input_string: The input string to parse.
#     :return: The parsed list.
#     """
#     result = []
#     current_item = ''
#     inside_quotes = False
#     escape_next = False
#     input_string = input_string.removeprefix('[').removesuffix(']')
#     for char in input_string:
#         if escape_next:
#             current_item += char
#             escape_next = False
#         elif char == '\\':
#             escape_next = True
#         elif char == "'" or char == '"':
#             inside_quotes = not inside_quotes
#         elif char == ',' and not inside_quotes:
#             result.append(current_item.strip())
#             current_item = ''
#         else:
#             current_item += char

#     if current_item.strip():
#         result.append(current_item.strip())

#     return result
    