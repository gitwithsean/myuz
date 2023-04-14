import openai
from abc import ABC, ABCMeta, abstractmethod
from phusis.models import *

class OpenAi():
    
    def gpt_completion_response(prompt, completion_config, model="text-ada-001"):
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

    def gpt_embeddings_response(input, model="text-embedding-ada-002"):
        response = openai.Embedding.create(
            model=model,
            input=input,
        )
        embeddings = response['data'][0]['embedding']
        return embeddings

def get_or_create_related_att_data(att_class, array_of_names):
    pprint(att_class)
    pprint(array_of_names)
    att_datas = []
    for n in array_of_names:
        obj, created = att_class.objects.get_or_create(name=n)
        att_datas.append(obj)
        pprint(obj)
    return att_datas

def complete_agent_definition(agent, agent_data):
    goals = get_or_create_related_att_data(AgentGoal, agent_data["goals"])
    agent.goals.set(goals),
    agent.roles.set(get_or_create_related_att_data(AgentRole, agent_data["roles"])),
    agent.qualifications.set(get_or_create_related_att_data(AgentQualification, agent_data["qualifications"])),
    agent.impersonations.set(get_or_create_related_att_data(AgentImpersonation, agent_data["impersonations"])),
    agent.personality.set(get_or_create_related_att_data(AgentTrait, agent_data["impersonations"])),
    agent.llelle=agent_data.get("elaboration", "")
    agent.malig=agent_data.get("elaboration", "")
    agent.subtr=agent_data.get("elaboration", "")
    
class AbstractEngineMeta(type(AbstractAgent), type(ABC)):
    pass

class AbstractEngine(AbstractAgent, ABC, metaclass=AbstractEngineMeta):
    agent_data = models.JSONField(default=dict)

    def __init__(self, agent_data):
        self = AbstractEngine.objects.get_or_create(agent_data["name"])
        self.agent_data = agent_data
        
    def submit_prompt():
        pass

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
    def handle_response():
        pass
      
    @abstractmethod  
    def hold_for_evaluation():
        pass
     
    @abstractmethod   
    def populate_db():
        pass   
        
    @abstractmethod
    def create_self_embedding():
        pass


class StructuralEngine(AbstractEngine):
    
    pass


def test_from_manager():
    agent_type = 'structural_agent'
    structural_agent_data = [       
        {   
            "name": "Plot outliner for a dark magical realism story",
            "goals": ["engaging", "mysterious", "captivating"],
            "roles": ["develop storyline", "combine magic", "real-world situations"],
            "qualifications": ["storytelling", "magical realism", "create dark narratives", "create complex narratives"],
            "impersonations": ["Gabriel García Márquez", "Isabel Allende", "Salman Rushdie", "Haruki Murakami", "Angela Carter"]
        },
        {
            "name": "Chapter outliner for a children's fantasy novel",
            "goals": ["compelling", "imaginative", "suitable for children"],
            "roles": ["develop chapter outline", "create fantastical elements", "memorable characters"],
            "qualifications": ["experience in writing children's literature", "strong imagination", "understanding of child development"],
            "impersonations": ["J.K. Rowling", "C.S. Lewis", "Roald Dahl", "Philip Pullman", "Madeleine L'Engle"]
        },
        {
            "name": "Someone who is experimental with narrative forms",
            "goals": ["challenge conventional storytelling", "innovative", "unconventional"],
            "roles": ["develop stories", "experiment with narrative techniques"],
            "qualifications": ["strong writing skills", "willingness to take risks", "background in experimental literature"],
            "impersonations": ["David Foster Wallace", "James Joyce", "Julio Cortázar", "Virginia Woolf", "Italo Calvino"]
        },
        {
            "name": "Someone who is successful for gripping plots with mediocre writing",
            "goals": ["captivate", "exciting", "suspenseful"],
            "roles": ["develop stories", "prioritize plot development", "pacing"],
            "qualifications": ["strong storytelling skills", "understanding of genre conventions", "ability to craft compelling plots"],
            "impersonations": ["Dan Brown", "E.L. James", "Stephenie Meyer", "Stieg Larsson", "James Patterson"]
        },
        {
            "name": "Someone who is critically acclaimed for their short stories",
            "goals": ["powerful", "impactful", "thought-provoking"],
            "roles": ["develop short stories", "rich characters", "evocative settings", "meaningful themes"],
            "qualifications": ["exceptional writing skills", "understanding of the short story form", "track record of critical acclaim"],
            "impersonations": ["Alice Munro", "Raymond Carver", "Flannery O'Connor", "Jhumpa Lahiri", "George Saunders"]
        }
    ]    
    
    structure_agents = []
    
    for agent_data in structural_agent_data:
        agent = StructuralAgent.objects.create(name=agent_data["name"])
        pprint(agent)
        agent.agent_type=agent_type
        complete_agent_definition(agent, agent_data)
        structure_agents.append(agent)
        
    for agent in structure_agents:
        print(agent.introduction)
        
        
        
                
five_examples_of = ["""
        Plot outliner for a dark magical realism story:

        Goal: To create an engaging, mysterious, and captivating plot that combines elements of magic and reality.
        Role: Develop a storyline that weaves together fantastical elements with real-world situations.
        Qualifications: Strong background in storytelling, experience with magical realism, and the ability to create dark and complex narratives.
        Examples: Gabriel García Márquez, Isabel Allende, Salman Rushdie, Haruki Murakami, and Angela Carter.""",
        """
        Chapter outliner for a children's fantasy novel:

        Goal: To create a compelling and imaginative story for children that features fantastical elements and memorable characters.
        Role: Develop a chapter-by-chapter outline for a children's novel with a focus on adventure, magic, and wonder.
        Qualifications: Experience in writing children's literature, a strong imagination, and an understanding of child development.
        Examples: J.K. Rowling, C.S. Lewis, Roald Dahl, Philip Pullman, and Madeleine L'Engle.
        """,
        """
        Someone who is experimental with narrative forms:

        Goal: To challenge conventional storytelling techniques and explore innovative narrative structures.
        Role: Develop stories with unconventional narrative techniques, such as non-linear timelines, multiple perspectives, or unusual formats.
        Qualifications: Strong writing skills, a willingness to take risks, and a background in experimental literature.
        Examples: David Foster Wallace, James Joyce, Julio Cortázar, Virginia Woolf, and Italo Calvino.
        """,
        """
        Someone who is wildly successful for stories with gripping plots, even if the writing is mediocre:

        Goal: To create stories that captivate readers with their exciting and suspenseful plots, even if the prose itself is not considered high literary art.
        Role: Develop stories that prioritize plot development and pacing, with a focus on keeping the reader engaged.
        Qualifications: Strong storytelling skills, an understanding of genre conventions, and an ability to craft compelling plots.
        Examples: Dan Brown, E.L. James, Stephenie Meyer, Stieg Larsson, and James Patterson.
        """,
        """
        Someone who is critically acclaimed for their short stories:
        Goal: To create powerful, impactful, and thought-provoking short stories that resonate with readers and critics alike.
        Role: Develop short stories with rich characters, evocative settings, and meaningful themes.
        Qualifications: Exceptional writing skills, an understanding of the short story form, and a track record of critical acclaim.
        Examples: Alice Munro, Raymond Carver, Flannery O'Connor, Jhumpa Lahiri, and George Saunders.
        """
    ]