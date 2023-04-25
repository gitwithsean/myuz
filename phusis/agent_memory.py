import uuid
import numpy as np
from scipy.spatial.distance import cosine
from apis import *
from django.db import models
import pinecone

class PineconeApi():
    pinecone_ = {}
    
    # Singleton
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        with open('./.secrets/pinecone_api_key', 'r') as f:
            pinecone_api_key = f.read()
        with open('./.secrets/pinecone_api_region', 'r') as f:
            pinecone_api_region = f.read()
            
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_api_region)
        dimension = 1536
        metric = "cosine"
        pod_type = "p1"
        table_name = "phusis"
    
        print(colored(f"PineconeApi.init(): Looking for {table_name} pinecone index...", "green"))
        if table_name not in pinecone.list_indexes():
            print(colored(f"PineconeApi.init(): Initializing new {table_name} pinecone index...", "green"))
            pinecone.create_index(
                table_name, dimension=dimension, metric=metric, pod_type=pod_type
            )
        self.index = pinecone.Index(table_name)

class ChatLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    prompt = models.TextField()
    repsonse = models.TextField()

class ProjectMemory():
    pinecone_api = PineconeApi()
    openai_api = OpenAiAPI()
    
    # Singleton
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add_chat_log_to_memory(self, text):
        chat_log = ChatLog.objects.create(message=text)
        chat_log_id = chat_log.id
        text_embeddings = self.openai_api.get_embedding_for(text)
        
        self.pinecone_api.upsert_embedding(items={str(chat_log_id): text_embeddings})
        
        
    def load_agents_memory_store_from_db(self):
        pass
    
    def search_memory_store(self, prompt, top_k=5):
        # Generate embeddings for the given prompt using the OpenAI API
        prompt_embeddings = self.openai_api.get_embedding_for(prompt)

        # Compute the cosine similarity between the prompt embeddings and the embeddings in the memory store
        similarities = []
        for stored_embedding in self.embeddings_memory_store:
            similarity = 1 - cosine(prompt_embeddings, stored_embedding["embeddings"])
            similarities.append({"message": stored_embedding["message"], "similarity": similarity})

        # Sort the results based on similarity, and return the top k results
        sorted_results = sorted(similarities, key=lambda x: x["similarity"], reverse=True)
        return sorted_results[:top_k]