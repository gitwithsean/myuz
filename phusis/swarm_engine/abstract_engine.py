import noveller.models, openai 
from abc import ABC, abstractmethod

class AbstractEngine(ABC):
    
    default_data = {
        "agent": noveller.models.Agent,
        "completion_config":{
            "temperature": 0.5,
            "max_tokens": 1000,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        },  
    }
    
    data = {}
    
    @abstractmethod
    def __init__(self, input=default_data):
        self.data = input
    
    @abstractmethod
    def select_model_to_work_on():
        pass
    
    @abstractmethod
    def getDataFromDb():
        pass
    
    @abstractmethod
    def buildPrompt():
        pass  
        
    @abstractmethod
    def choose_model_for_prompt():
        pass
    
    @abstractmethod
    def submit_prompt():
        pass
     
    @abstractmethod   
    def handle_response():
        pass
      
    @abstractmethod  
    def hold_for_evaluation():
        pass
     
    @abstractmethod   
    def populate_db():
        pass   
      
    def gpt_response(model, prompt, completion_config):
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            temperature=completion_config["temperature"],
            max_tokens=completion_config["max_tokens"],
            top_p=completion_config["top_p"],
            frequency_penalty=completion_config["frequency_penalty"],
            presence_penalty=completion_config["presence_penalty"]
        )
        return response
