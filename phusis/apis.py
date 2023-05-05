import openai
from termcolor import colored
from .agent_utils import memorize_chat


class OpenAiAPI():
    api = openai
    
    def __init__(self):
        with open('./.secrets/openai_api_key', 'r') as f:
            openai.api_key = f.read()
    
    def chat_response(self, api_data):
        
        self.api.api_key = api_data['key']
        
        # print(colored("\nOpenAiApi.chat_response(): Submitting chat completion\n", "yellow"))
        
        #hardocding it fpr now
        api_data['model'] = 'gpt-4'
        
        completion = openai.ChatCompletion.create(
            model=api_data['model'],
            messages=api_data['messages_to_submit']
        )
        
        # print(colored("\nOpenAiApi.chat_response(): Response received\n", "green"))
        # print(colored(f"\n{completion}\n", "green"))
        return completion
    
    def gpt_chat_response(self, api_data):
        prompting_agent = api_data['prompting_agent']
        responding_agent = api_data['responding_agent']
        system_message = ""
        
        if responding_agent.agent_type == "orchestration_agent":
            key_file = f"./.secrets/orc_openai_api_key"
            model = "gpt-4"
        else:
            key_file = f"./.secrets/openai_api_key"
            model = "gpt-3.5-turbo"
            
        with open(key_file, 'r') as f:
                openai.api_key = f.read()

        if api_data.get('system_message') != None:
            system_message = api_data['system_message']
        elif responding_agent.wake_up_message != '':
            system_message = responding_agent.wake_up_message
           
        messages_to_submit = [{"role": "system", "content": system_message}]
        
        if responding_agent != "UtilityAgent":
            i = 3
            if responding_agent.chat_logs.all() != [] :
                for chat_log in responding_agent.chat_logs.all(): 
                    #some way to count the tokens in the chat log and not add if it goes beyond a limit, but for now, just the last i (3)
                    if i > 0:
                        for obj in chat_log.convert_log_to_chain_objects():
                            messages_to_submit.append(obj)
                            i = i - 1
        
        messages_to_submit.append({"role": "user", "content": api_data.get("content")})
        
        print(colored(f"\n\nOpenAi.gpt_chat_response(): messages_to_submit = \n\n{messages_to_submit}\n\n", "yellow"))

        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages_to_submit
        )
        
        print(colored(f"OpenAi.gpt_chat_response(): response = \n\n{completion.choices[0].message.content}", "green"))
        
        if api_data['responding_agent'] != "UtilityAgent":
            new_chat_log = responding_agent.add_to_chat_logs(api_data.get("content"), completion.choices[0].message.content) 
            memorize_chat(new_chat_log)
        
        return completion.choices[0].message.content

    
    def get_embeddings_for(self, input, model="text-embedding-ada-002"):
        response = openai.Embedding.create(
            model=model,
            input=input,
        )
        return response['data'][0]['embedding']