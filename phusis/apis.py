import openai, time, json
from pprint import pprint
from termcolor import colored
from django.apps import apps
from .agent_utils import memorize_chat
from .secret_sauce import ph
from .secret_sauce import quora


class OpenAiAPI():
    openai.api_key
    
    def __init__(self):
        with open('./.secrets/openai_api_key', 'r') as f:
            openai.api_key = f.read()
    
    def get_embeddings_for(self, input, model="text-embedding-ada-002"):
        response = openai.Embedding.create(
            model=model,
            input=input,
        )
        return response['data'][0]['embedding']
    
    def gpt_chat_response(self, api_data, max_retries=3, delay=1):

        prompting_agent = api_data['prompting_agent']
        responding_agent = api_data['responding_agent']
        last_exception = None
        retry_attempt = 1
        system_message = ""
        if not responding_agent.agent_type == 'orchestration_agent':
            system_message = "You are one of many AI agents in a swarm working on a human user project. Each of you specialize in different set of skills and responsibilities. Most of your interactions will be with the Orchestration Agent, your project manager, but you will also hear from other agents and/or the user."
        else:
            system_message = "You are the master orchestrator of a swarm of GPT agents, all working towards a common objective. You will be communicating with the user to get, clarify and suggest modifications to the overall project and how it is being executed. And you will be communicating with other agents to evaluate and set their tasks."
        
                
        messages_to_submit = [{"role": "system", "content": system_message}]
        
        i = 3
        if responding_agent.chat_logs != None :
            for chat_log in responding_agent.chat_logs.all(): 
                #some way to count the tokens in the chat log and not add if it goes beyond a limit, but for now, just the last i (3)
                if i > 0:
                    for obj in chat_log.convert_log_to_chain_objects():
                        messages_to_submit.append(obj)
                        i = i - 1
        
        messages_to_submit.append({"role": "user", "content": api_data.get("content")})
        
        print(colored(f"\n\nOpenAi.gpt_chat_response(): messages_to_submit = {messages_to_submit}\n\n", "green"))
        
        # messages_to_submit_str = json.dumps(messages_to_submit, ensure_ascii=True)
         
        # print(colored(f"OpenAi.gpt_chat_response(): messages_to_submit_str = {messages_to_submit_str}", "green"))
                         
        # for retry_attempt in range(max_retries):
        #     try:
        completion = openai.ChatCompletion.create(
            model=api_data.get('model', "gpt-3.5-turbo"),
            messages=messages_to_submit
        )
        
        # print(colored(f"OpenAi.gpt_chat_response(): completion = {completion}", "green"))
        
        new_chat_log = responding_agent.add_to_chat_logs(api_data.get("content"), completion.choices[0].message.content)                

        memorize_chat(new_chat_log)
        
        return completion.choices[0].message.content
        
            # except Exception as e:
            #     last_exception = e
            #     time.sleep(delay)  
            #     retry_attempt = retry_attempt + 1 # Wait for the specified delay before retrying

        # If the function reaches this point, it means all retries have failed
        raise last_exception

class phApi():
    # set cf_clearance cookie (needed again)
    ph.cf_clearance = 'xx.xx-1682166681-0-160'
    ph.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' # same as the one from browser you got cf_clearance from
    
    def gpt_chat_response(self, api_data, max_retries=3, delay=1):
        # print(f"OpenAi.gpt_chat_response(): api_data =  {api_data}")
        prompting_agent = api_data['prompting_agent']
        responding_agent = api_data['responding_agent']
        last_exception = None
        retry_attempt = 1
        system_message = ""
        if not responding_agent.agent_type == 'orchestration_agent':
            system_message = "You are one of many AI agents in a swarm working on a human user project. Each of you specialize in different set of skills and responsibilities. Most of your interactions will be with the Orchestration Agent, your project manager, but you will also hear from other agents and/or the user."
        else:
            system_message = "You are the master orchestrator of a swarm of GPT agents, all working towards a common objective. You will be communicating with the user to get, clarify and suggest modifications to the overall project and how it is being executed. And you will be communicating with other agents to evaluate and set their tasks."
            
        messages_to_submit = [{"role": "system", "content": system_message},
        ]
        
        #NEED TO DO SOME CHAT CHAINING HERE      
        
        messages_to_submit.append({"role": "user", "content": api_data.get("content")})
        
        print(colored(f"OpenAi.gpt_chat_response(): messages_to_submit = {messages_to_submit}", "green"))
        
        messages_to_submit_str = json.dumps(messages_to_submit, ensure_ascii=True)
         
        # print(colored(f"OpenAi.gpt_chat_response(): messages_to_submit_str = {messages_to_submit_str}", "green"))
         
        for retry_attempt in range(max_retries):
            try:
                result = ph.Completion.create(
                    model  = 'gpt-4',
                    prompt = messages_to_submit_str,
                    results     = ph.Search.create(messages_to_submit_str, actualSearch = False), # create search (set actualSearch to False to disable internet)
                    creative    = True,
                    detailed    = True,
                    codeContext = f'{system_message}') # up to 3000 chars of code
                
                print(result)
                    
                return result.completion.choices[0].text
            except Exception as e:
                last_exception = e
                time.sleep(delay)  
                retry_attempt = retry_attempt + 1 # Wait for the specified delay before retrying

        # If the function reaches this point, it means all retries have failed
        raise last_exception
    
    
class quoraApi(): 
    models = {
        'sage'   : 'capybara',
        'gpt-4'  : 'beaver',
        'claude-v1.2'         : 'a2_2',
        'claude-instant-v1.0' : 'a2',
        'gpt-3.5-turbo'       : 'chinchilla'
    }    
    token = ''
    model = {}

    def gpt_chat_response(self, api_data, max_retries=3, delay=1):
        if not self.token:
            self.token = quora.Account.create(logging = True, enable_bot_creation=True)
        
        # print(f"api_data =  {api_data}")
        prompting_agent = api_data['prompting_agent']
        responding_agent = api_data['responding_agent']
        last_exception = None
        retry_attempt = 1
        system_message = ""
        if not responding_agent.agent_type == 'orchestration_agent':
            system_message = "You are one of many AI agents in a swarm working on a human user project. Each of you specialize in different set of skills and responsibilities. Most of your interactions will be with the Orchestration Agent, your project manager, but you will also hear from other agents and/or the user."
        else:
            system_message = "You are the master orchestrator of a swarm of GPT agents, all working towards a common objective. You will be communicating with the user to get, clarify and suggest modifications to the overall project and how it is being executed. And you will be communicating with other agents to evaluate and set their tasks."
            
        messages_to_submit = [{"role": "system", "content": system_message},
        ]
        
        #NEED TO DO SOME CHAT CHAINING HERE      
        
        messages_to_submit.append({"role": "user", "content": api_data.get("content")})
        
        print(colored(f"OpenAi.gpt_chat_response(): messages_to_submit = {messages_to_submit}", "green"))
        
        messages_to_submit_str = json.dumps(messages_to_submit, ensure_ascii=True)
         
        # print(colored(f"OpenAi.gpt_chat_response(): messages_to_submit_str = {messages_to_submit_str}", "green"))
        
        # model = quora.Model.create(
        #     token = self.token,
        #     model = 'gpt-4', # or claude-instant-v1.0
        #     system_prompt = f'{system_message}' 
        # )


         
        for retry_attempt in range(max_retries):
            try:
                response = quora.Completion.create(
                    model  = 'gpt-4',
                    prompt = messages_to_submit_str,
                    token  = self.token,
                    system_prompt = f'{system_message}'
                )
                
                print(colored(f"\n\nRESPONSE: {response}\n\n", "green"))
                print(colored(f"RESPONSE TEXT: {response.completion.choices[0].text}", "green"))      
                return response.completion.choices[0].text
            except Exception as e:
                last_exception = e
                time.sleep(delay)  
                retry_attempt = retry_attempt + 1 # Wait for the specified delay before retrying

        # If the function reaches this point, it means all retries have failed
        raise last_exception

    def __init__(self): 
        # create account
        # make sure to set enable_bot_creation to True
        token = quora.Account.create(logging = True, enable_bot_creation=True)

        self.model = quora.Model.create(
            token = token,
            model = 'gpt-4', # or claude-instant-v1.0
            system_prompt = '' 
        )
        

    