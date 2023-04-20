import openai, pinecone, os, shutil
from pprint import pprint
from termcolor import colored
from django.apps import apps

class OpenAi():
    openai.api_key
    
    def __init__(self):
        with open('./.secrets/openai_api_key', 'r') as f:
            openai.api_key = f.read()
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

    def get_embedding_for(self, input, model="text-embedding-ada-002"):
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

class PineconeApi():
    index = {}
        
    # _instance = None
    # def __new__(cls):
    #     if cls._instance is None:
    #         # print('Creating PineconeApi singleton instance')
    #         cls._instance = super().__new__(cls)
    #         # Initialize the class attributes here
    #         cls._instance.prompts_since_reminder = 0
    #         cls._instance.max_prompts_between_reminders = 5
    #     return cls._instance
    
    # print(colored(f"PineconeApi.init(): Initializing pinecone api...", "green"))
    # def __init__(self):
    #     with open('./.secrets/pinecone_api_key', 'r') as f:
    #         pinecone_api_key = f.read()
    #     with open('./.secrets/pinecone_api_region', 'r') as f:
    #         pinecone_api_region = f.read()

    #     pinecone.init(api_key=pinecone_api_key, environment=pinecone_api_region)
    #     dimension = 1536
    #     metric = "cosine"
    #     pod_type = "p1"
    #     table_name = "phusis"
    
    #     print(colored(f"PineconeApi.init(): Looking for {table_name} pinecone index...", "green"))
    #     if table_name not in pinecone.list_indexes():
    #         print(colored(f"PineconeApi.init(): Initializing new {table_name} pinecone index...", "green"))
    #         pinecone.create_index(
    #             table_name, dimension=dimension, metric=metric, pod_type=pod_type
    #         )
    #     self.index = pinecone.Index(table_name)
    
    def upsert_embedding(self, text_data):
        print(colored(f"PineconeApi.upsert_embedding(): Beginning upsert ...\"", "green"))
        content = ""
        path_to_loaded_file = ""
        print_to_console_content = ""
        if 'local_file_path' in text_data:
            # If it's a file, there's a chance it's so big it will hinder performance of the db
            # so we'll just copy the file to a 'pinecone_loaded' sub dir of the directory it's in
            # and give the db entry the path to the file in its loaded dir to load on demand
            current_file_dir = os.path.dirname(text_data['local_file_path'])
            file_name = os.path.basename(text_data['local_file_path'])            
            loaded_files_dir = os.path.join(current_file_dir, "pinecone_loaded")
            path_to_loaded_file = os.path.join(loaded_files_dir, file_name)
            
            os.makedirs(loaded_files_dir, exist_ok=True)
            # os.cop(text_data['local_file_path'], path_to_loaded_file)
            shutil.copy(text_data['local_file_path'], loaded_files_dir)
            content = path_to_loaded_file
            print_to_console_content = path_to_loaded_file
        else:
            content = text_data['content']     
            print_to_console_content = f"{content[0]} {content[1]} {content[2]} {content[3]}"
        
        print(colored(f"PineconeApi.upsert_embedding(): Loading embedding for content \"{print_to_console_content} to local db...\"", "green")) 
        vector_class = apps.get_model('phusis', 'Vector') 
        existing_vector = vector_class.objects.filter(content=print_to_console_content).first()
        
        if existing_vector:
            print(colored(f"PineconeApi.upsert_embedding(): Vector already exists for content \"{print_to_console_content}\" in local db. Skipping... {self.index}...\"", "yellow")) 
        else:
            new_vector = vector_class()
            new_vector.content = content
            new_vector.embeddings = text_data['embeddings']
            new_vector.save()
            new_vector_id = str(new_vector.id)
            response = {}
            try:
                print(colored(f"PineconeApi.upsert_embedding(): Upserting embedding for content \"{print_to_console_content} to pinecone index {self.index}...\"", "green"))
                response = self.index.upsert([(new_vector_id, text_data['embeddings'], {"raw_text": f"{content}"})]) 
                pprint(response)
                return f"text_data upserted, Vector {new_vector_id} saved to local db"
            except Exception as e:
                print(colored(f"PineconeApi.upsert_embedding(): Failure loading embedding for content \"{content}\"\n\nDeleting vector", "red"))
                #delete the new Vector
                vector_class.objects.get(id=new_vector_id).delete()
                if os.path.isfile(path_to_loaded_file):
                    #delete the copied file
                    os.remove(path_to_loaded_file)
                pprint(e)
                # pprint(f"content {content}")   
                # pprint(new_vector)
                # pprint(f"new_vector {new_vector}")
                # pprint(f"new_vector.embeddings {new_vector.embeddings}")
                # pprint(f"new_vector.content {new_vector.content}")  
                # print(f"new_vector_id {new_vector_id}")
            
