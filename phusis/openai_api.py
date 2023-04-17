import openai
from pprint import pprint

class OpenAi():
    
    def __init__(self):
        pass
    
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

    def gpt_embeddings_response(self, input, model="text-embedding-ada-002"):
        response = openai.Embedding.create(
            model=model,
            input=input,
        )
        return response['data'][0]['embedding']
    
    def gpt_chat_response(self, api_data):
        # print(f"api_data =  {api_data}")
        completion = openai.ChatCompletion.create(
            model=api_data.get('model', "gpt-3.5-turbo"),
            messages=[
                {
                    "role": "user", 
                    "content": api_data.get("content")
                }
            ]
        )
        return completion.choices[0].message
    {
}
