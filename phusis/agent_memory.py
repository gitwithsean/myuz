from pprint import pprint
import uuid, textract, re
from scipy.spatial.distance import cosine
from .agent_utils import get_embeddings_for
from django.db import models
import pinecone
from termcolor import colored

class Vector(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    vector_id = models.CharField(max_length=200, default='', blank=False, null=False)
    embeddings = models.JSONField(default=list, blank=True, null=True)
    vector_metadata = models.JSONField(default=list, blank=True, null=True)
    
    def __init__(self, vector_id='', embeddings=[], vector_metadata={}):
        self.vector_id = str(vector_id)
        self.embeddings = embeddings
        self.vector_metadata = vector_metadata
    
    def for_upsert(self):
        if self.vector_metadata:
            return (self.vector_id, self.embeddings, self.vector_metadata)
        else:
           return (self.vector_id, self.embeddings,)     


class PineconeApi():
    index = None
    
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

    def upsert_embedding(self, vector_id, embeddings, vector_metadata={}):
        vector = Vector(vector_id=vector_id, embeddings=embeddings, vector_metadata=vector_metadata)
        self.index.upsert([vector.for_upsert()])
        return [vector]
        
    def upsert_embeddings(self, objects):
        vectors_to_upsert = []
        
        print(colored(f"PineconeApi.upsert_embeddings(): Creating {len(objects)} vector objects to upsert...", "green"))
        
        for obj in objects:
            vector = Vector(vector_id=obj['id'], embeddings=obj['embeddings'], vector_metadata=obj['vector_metadata'])
            vectors_to_upsert.append(vector.for_upsert())
        
        print(colored(f"PineconeApi.upsert_embeddings(): Vectors created...", "green"))
        # pprint(vectors_to_upsert)
           
        self.index.upsert(vectors_to_upsert)
        return vectors_to_upsert


class FileParagraph(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    path_to_file = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)


class ProjectMemory():
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    project_vectors = models.ManyToManyField(Vector, blank=True)


    def add_chat_log_to_memory(self, prompt, response, responder):
        
        from .agent_models import ChatLog
        chat_log = ChatLog.objects.create(prompt=prompt, response=response, responder_id=responder.id, responder_name=responder.name, responder_type=responder.agent_type)
        chat_log_id = chat_log.id
        text_embeddings = get_embeddings_for(f"Prompt: {prompt}\nResponder: {responder.id} {responder.agent_type} {responder.name}:\nResponse: {response}")
        
        PineconeApi().upsert_embedding(chat_log_id, text_embeddings)
    
    def add_chat_log_db_instance_to_pinecone_memory(self, chat_log):
        chat_log_id = chat_log.id
        prompt = chat_log.prompt
        responder_id = chat_log.responder_id
        responder_type = chat_log.responder_type
        response = chat_log.response
        responder_name = chat_log.responder_name
        
        text_embeddings = get_embeddings_for(f"Prompt: {prompt}\nResponder: {responder_id} {responder_type} {responder_name}:\n Response: {response}")
        
        PineconeApi().upsert_embedding(chat_log_id, text_embeddings)
        
    def add_file_to_memory(self, path_to_file):
        print(colored(f"ProjectMemory.add_file_to_memory(): Adding {path_to_file} to memory...", "yellow"))
        paragraphs = self.extract_text_and_split_into_paragraphs(path_to_file)
        objects_to_upsert = []
        metadata = self.get_project_vector_metadata()
        metadata["path_to_file"] = path_to_file
        i=0
        for paragraph in paragraphs:
            i += 1
            print(colored(f"ProjectMemory.add_file_to_memory(): Getting embeddings for paragraph {paragraph[:50]}...", "yellow"))
            paragraph_embeddings = get_embeddings_for(paragraph)
            paragraph_obj = FileParagraph.objects.create(path_to_file=path_to_file, text=paragraph)
            paragraph_obj_id = paragraph_obj.id
            metadata["paragraph_num"] =  f"{i}"
            objects_to_upsert.append({"id": paragraph_obj_id, "embeddings": paragraph_embeddings, "vector_metadata": metadata})
        
        print(colored(f"ProjectMemory.add_file_to_memory(): upserting vector data for the paragraphs to pinecone", "yellow"))
        PineconeApi().upsert_embeddings(objects_to_upsert)
        
    def search_memory_store(self, prompt, top_k=5):
        # Generate embeddings for the given prompt using the OpenAI API
        prompt_embeddings = get_embeddings_for(prompt)

        # Compute the cosine similarity between the prompt embeddings and the embeddings in the memory store
        similarities = []
        for stored_embedding in self.embeddings_memory_store:
            similarity = 1 - cosine(prompt_embeddings, stored_embedding["embeddings"])
            similarities.append({"message": stored_embedding["message"], "similarity": similarity})

        # Sort the results based on similarity, and return the top k results
        sorted_results = sorted(similarities, key=lambda x: x["similarity"], reverse=True)
        return sorted_results[:top_k]
    
    def extract_text_and_split_into_paragraphs(self, file_path):
             
        print(colored(f"ProjectMemory.extract_text_and_split_into_paragraphs(): Extracting paragraphs from {file_path}", "yellow"))
        
        content = textract.process(file_path).decode('utf-8')
        content = content.replace('\r', '\n')
        
        # Use regular expressions to split the text into paragraphs
        paragraphs = re.split(r'\n\s*\n', content)

        # Keep only paragraphs with at least one alphabetical character
        paragraphs = [p.strip() for p in paragraphs if p.strip() and re.search('[a-zA-Z]', p)]

        print(colored(f"ProjectMemory.extract_text_and_split_into_paragraphs(): {paragraphs.__len__()} paragraphs extracted from {file_path}, here's the first one...", "green"))
        print(colored(f"{paragraphs[0]}", "green"))

        return paragraphs
    
    
    # def get_text_paragraphs_from_any_file(self, path_to_file):
    #     _, file_extension = os.path.splitext(path_to_file)

    #     if file_extension.lower() == '.pdf':
    #         return self.split_content_into_paragraphs_list(self.read_pdf_content(path_to_file))
    #     elif file_extension.lower() == '.txt':
    #         return self.split_content_into_paragraphs_list(self.read_txt_content(path_to_file))
    #     elif file_extension.lower() == '.md':
    #         return self.split_content_into_paragraphs_list(self.read_md_content(path_to_file))
    #     else:
    #         raise ValueError(f"Unsupported file type: {file_extension}")
     
        
    # def read_pdf_content(self, file_path):
    #     with open(file_path, 'rb') as f:
    #         pdf_reader = PyPDF2.PdfFileReader(f)
    #         return "\n".join([pdf_reader.getPage(i).extractText() for i in range(pdf_reader.numPages)])


    # def read_txt_content(self, file_path):
    #     with open(file_path, 'r') as f:
    #         return f.read()


    # def read_md_content(self, file_path):
    #     with open(file_path, 'r') as f:
    #         md_content = f.read()
    #         html_content = markdown(md_content)
    #         soup = BeautifulSoup(html_content, 'html.parser')
    #         return soup.get_text()
    
    # def split_content_into_paragraphs_list(content):
    #     lines = content.split('\n')
    #     paragraphs = []
    #     current_paragraph = []

    #     for line in lines:
    #         stripped_line = line.strip()
    #         if len(stripped_line) == 0:
    #             if current_paragraph:
    #                 paragraphs.append('\n'.join(current_paragraph))
    #                 current_paragraph = []
    #         else:
    #             if not current_paragraph and stripped_line.startswith(' '):
    #                 # This line might be a continuation of the previous paragraph, so we'll join it
    #                 if paragraphs:
    #                     paragraphs[-1] += ' ' + stripped_line
    #             else:
    #                 current_paragraph.append(line)

    #     if current_paragraph:
    #         paragraphs.append('\n'.join(current_paragraph))

    #     # Filter out empty paragraphs (only whitespace characters)
    #     paragraphs = [p for p in paragraphs if p.strip()]

    #     return paragraphs
