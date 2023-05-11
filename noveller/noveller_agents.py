from phusis.agent_models import AbstractAgent, OrchestrationAgent
from .noveller_engines import WritingAgentEngine

class OrchestrationAgent(OrchestrationAgent):
    pass

class WritingAgent(AbstractAgent, WritingAgentEngine):
    type_description = """
    Agent class concerned with:
        * producing the final written drafts of paragraphs, scenes, parts, chapters etc.
    """
    agent_type = "writing_agent"
    class_display_name = "Writing Agent"
    phusis_applicaton = "noveller"


class PoeticsAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
        * narrative technique
        * poetic literacy
        * literary/linguistic theory
        * metaphoric / analogistic approaches to the content 
    """
    agent_type = "poetics_agent"
    class_display_name = "Poetics Agent"
    phusis_applicaton = "noveller"


class StructuralAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
    - story plotting
    - story structure (r.g. experimental and/or tried and tested structures)
    - scene sequencing
    - fleshing out the story structure and plotting based on the inputs from other agents in the swarm  
    """
    agent_type = "structural_agent"
    class_display_name = "Structural Agent"
    phusis_applicaton = "noveller"


class SceneAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
    - bringing together the work of the thematic, structural, world building, character and other agents to collaboratively flesh out scenes
    """
    agent_type = "scene_agent"
    class_display_name = "Scene Agent"  
    phusis_applicaton = "noveller"  

 
class ResearchAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
    - taking a subject area and a project goal, and thinking of research topics that could be researched for the book, 
    - how to plan, structure and initially approach that research
    - like an expert librarian, knowing or knowing how to find the best sources for researching a topic
    - doing the background research on those specific topics to an expert degree
    """
    agent_type = "research_agent"
    class_display_name = "Research Agent"
    phusis_applicaton = "noveller"


class CharacterAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
    - fleshing out character profiles
    - 'becoming' the character so that a user or other agents can talk to them, produce dialog, discuss decisions, etc.
    """
    agent_type = "character_agent"
    class_display_name = "Character Agent"
    phusis_applicaton = "noveller"

    
class WorldBuildingAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
    - building the world of the story
    """
    agent_type = "world_building_agent"
    class_display_name = "World Building Agent"
    phusis_applicaton = "noveller"
  
    
class ThemeExploringAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
    - considering the possible themes of the story and adding Theme objects to the story
    - diving deeper into the theme objects to provide insight into how they might influcen the story
    - informing other agents on how they could improve their work to better serve the themes
    """
    agent_type = "theme_exploring_agent"
    class_display_name = "Theme Exploring Agent" 
    phusis_applicaton = "noveller"
   
    
class ConflictAndResolutionAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
    - setting conflicts within the story to drive plot
    - conflicts between characters, the world, themes, events, internal, etc.
    """
    agent_type = "conflict_and_resolution_agent"
    class_display_name = "Conflict And Resolution Agent"  
    phusis_applicaton = "noveller"
  
    
class InterdisciplinaryAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
    - These are relatively neutral agents that would consider the output from all agents in a swarm and make sure they are not deviating from each other, making sure that each of them are serving towards a common goal in a cohesive way, that research informs setting, informs themes, informs style etc. Not quite like a director of a film, more like assistant directors
    - They will provide 'grades' to what is produced, but less about quality and more about how close they are to cohering with the work of the other agents working in different disciplines. With 0.5 being neutral, 1 being exemplary and 0 meaning heading in the wrong direction. 
    """
    agent_type = "interdisciplinary_agent"
    class_display_name = "Interdisciplinary Agent"
    phusis_applicaton = "noveller"
    
    
class QualityEvaluationAgent(AbstractAgent):
    type_description = """
    Agent class concerned with:
    - evaluating the output and work of each of the agents.
    """
    agent_type = "quality_evaluation_agent"
    class_display_name = "Quality Evaluation Agent"
    phusis_applicaton = "noveller"
    