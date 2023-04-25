import openai, time
from pprint import pprint
from termcolor import colored
from django.apps import apps


class OpenAiAPI():
    openai.api_key
    
    def __init__(self):
        with open('./.secrets/openai_api_key', 'r') as f:
            openai.api_key = f.read()
            
    
    def gpt_completion_response(self, prompt, data):
        response = openai.Completion.create(
            engine=data.get('model','text-ada-001'),
            prompt=prompt,
            temperature=data.get('temperature', 0.2),
            max_tokens=data.get("max_tokens", 300),
            top_p=data.get("top_p", 1),
            frequency_penalty=data.get("frequency_penalty", 0),
            presence_penalty=data.get("presence_penalty", 0),
        )

        
        return response['choices'][0]['text']


    def get_embedding_for(self, input, model="text-embedding-ada-002"):
        response = openai.Embedding.create(
            model=model,
            input=input,
        )
        return response['data'][0]['embedding']
    

    def gpt_chat_response(self, api_data, max_retries=3, delay=1):
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
        
        if responding_agent.script_for == None:
            pass
        else:
            previous_chats = responding_agent.script_for.convert_last_n_number_of_entries_to_api_format(5) 

            if previous_chats == []:
                pass
            else:
                for chat in previous_chats:
                    messages_to_submit.append(chat)                 
        
        messages_to_submit.append({"role": "user", "content": api_data.get("content")})
        
        print(colored(f"OpenAi.gpt_chat_response(): messages_to_submit = {messages_to_submit}", "green"))
        
        # messages_to_submit_str = json.dumps(messages_to_submit, ensure_ascii=True)
         
        # print(colored(f"OpenAi.gpt_chat_response(): messages_to_submit_str = {messages_to_submit_str}", "green"))
         
        for retry_attempt in range(max_retries):
            try:
                completion = openai.ChatCompletion.create(
                    model=api_data.get('model', "gpt-3.5-turbo"),
                    messages=messages_to_submit
                )
                print(colored(f"OpenAi.gpt_chat_response(): completion = {completion}", "green"))
                return completion.choices[0].message
            except Exception as e:
                last_exception = e
                time.sleep(delay)  
                retry_attempt = retry_attempt + 1 # Wait for the specified delay before retrying

        # If the function reaches this point, it means all retries have failed
        raise last_exception
