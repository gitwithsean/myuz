from __future__ import annotations
from pprint import pprint
from django.db import models
from phusis.agent_models import AbstractPhusisProject, AbstractPhusisProjectAttribute
from django.apps import apps
from abc import abstractmethod
from termcolor import colored


class NovellerModelDecorator(AbstractPhusisProjectAttribute):
    elaboration = models.TextField(blank=True, null=True)
    
    class Meta:
        abstract = True
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    
    def to_short_dict(self):
        return {
            "id": str(self.id),
            "name" : self.name,
        }
        
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
        }
    
    @abstractmethod
    def get_brief():
        pass
    
    # NovellerModelDecorator set_data
    def set_data(self, properties_dict):
        """
        Set the data for the instance based on the provided properties dictionary.
        
        Args:
            properties_dict (dict): A dictionary containing the properties to set for the instance.
        """
        # pprint(properties_dict)
        for key, value in properties_dict.items():
            # Get the field instance
            field = self._meta.get_field(key)
            # print(f"key: {key}\nvalue: {value}\nfield: {field}\n")
            if isinstance(field, models.ManyToManyField):
                related_objects = []
                # print(f"key: {key}\nvalue: {value}\nfield: {field}\n")
                # Find the related objects using find_attribute_by function
                if isinstance(value, list):
                    for attr_name in value:
                        # print(f"{field.related_model} {attr_name}")
                        attr_clas, attr_instance = find_and_update_or_create_attribute_by(attr_name, field.related_model)
                        related_objects.append(attr_instance)
                else:
                    # print(f"{field.related_model} {attr_name}")
                    attr_clas, attr_instance = find_and_update_or_create_attribute_by(value, field.related_model)
                    related_objects.append(attr_instance)            

                # Set the related objects to the attribute
                getattr(self, key).set(related_objects)
            elif isinstance(field, models.ForeignKey):
                attr_clas, attr_instance = find_and_update_or_create_attribute_by(value, field.related_model)
                setattr(self, key, attr_instance)
            else:
                # Handle other attribute types as needed
                
                # print(f"key: {key}\nvalue: {value}\nfield: {field}\n")
                setattr(self, key, value)
        self.save()        
        

class Location(NovellerModelDecorator):
    pass


class LiteraryInspiration(NovellerModelDecorator):
    pass


class StoryTeller(NovellerModelDecorator):
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE, null=True)
    lit_style_guide = models.ForeignKey('LiteraryStyleGuide', on_delete=models.CASCADE, null=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "teller": {
                "id": str(self.character_version.id),
                "who_and_when": self.character_version.name    
            },
            "literary_style": self.lit_style_guide.name
        }
    
    # def __str__(self):
    #     return f"{self.character_version} style as a story teller"
    
    class Meta:
        ordering = ['character_version__for_character__name']


class LiteraryTheme(NovellerModelDecorator):
    pass


class NarrativePerspective(NovellerModelDecorator):
    pass


class LiteraryTrait(NovellerModelDecorator):
    pass


class LiteraryTone(NovellerModelDecorator):
    pass


class LiteraryMood(NovellerModelDecorator):
    pass


class LiteraryImagery(NovellerModelDecorator):
    pass


class LiterarySymbolism(NovellerModelDecorator):
    pass


class StoryPacing(NovellerModelDecorator):
    pass


class LiteraryStyleGuide(NovellerModelDecorator):
    perspective = models.ForeignKey(NarrativePerspective, on_delete=models.CASCADE, null=True)
    inspirations = models.ManyToManyField(LiteraryInspiration, blank=True)
    tone = models.ManyToManyField(LiteraryTone, blank=True)
    imagery = models.ManyToManyField(LiteraryImagery, blank=True)
    symbolism = models.ManyToManyField(LiterarySymbolism, blank=True)
    traits = models.ManyToManyField(LiteraryTrait, related_name='litstyleguide_traits', blank=True)
    traits_to_avoid = models.ManyToManyField(LiteraryTrait, related_name='litstyleguide_avoid', blank=True)
    style_guide = models.TextField(blank=True, null=True)
    compressed_sg = models.TextField(blank=True, null=True)
    writing_samples = models.TextField(blank=True, null=True)


    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "narrative_perspective": self.perspective.name,
            "inspirations": [insp.to_short_dict() for insp in self.inspirations.all()],
            "tone": [tone.to_short_dict() for tone in self.tone.all()],
            "imagery": [img.to_short_dict() for img in self.imagery.all()],
            "symbolism": [sym.to_short_dict() for sym in self.symbolism.all()],
            "traits": [trait.to_short_dict() for trait in self.traits.all()],
            "traits_to_avoid": [trait.to_short_dict() for trait in self.avoid.all()],
            "style_guide": self.style_guide,
        }


class Genre(NovellerModelDecorator):
    pass

    
class TargetAudience(NovellerModelDecorator):
    pass


class BackgroundEvent(NovellerModelDecorator):
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_story_events = models.IntegerField(blank=True, null=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "order_in_story_events": self.order_in_story_events,
        }
    

class Faction(NovellerModelDecorator):
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField('CharacterVersion', blank=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "faction_members": [member.to_short_dict() for member in self.members.all()]
        }
    
    
class DeeperBackgroundResearchTopic(NovellerModelDecorator):
    notes = models.TextField(blank=True, null=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "notes": self.notes,
        }
    

class BackgroundResearch(NovellerModelDecorator):
    research = models.TextField(blank=True)
    deeper_research_topics = models.ManyToManyField(DeeperBackgroundResearchTopic, blank=True)
    
    def to_short_dict(self):              
        return {
            "id": str(self.id),
            "name" : self.name,
            "deeper_research_topics": [topic.to_short_dict() for topic in self.deeper_research_topics.all()],
        }
    
    def to_dict(self):              
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "deeper_research_topics": [topic.to_short_dict() for topic in self.deeper_research_topics.all()],
        }
    
class Setting(NovellerModelDecorator):
    books = models.ManyToManyField('Book', blank=True)
    background_events = models.ManyToManyField(BackgroundEvent, blank=True)
    factions = models.ManyToManyField(Faction, blank=True)
    background_research = models.OneToOneField(BackgroundResearch, on_delete=models.SET_NULL, blank=True, null=True)
    general_setting = models.TextField(blank=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "background_events": [event.to_short_dict() for event in self.background_events.all()],
            "factions": [faction.to_short_dict() for faction in self.factions.all()],
            "background_research": self.background_research.to_short_dict(),
            "general_setting": self.general_setting,
        }
        
class Scene(NovellerModelDecorator):
    for_plot = models.ForeignKey('Plot', related_name='plots_scenes', blank=True, on_delete=models.SET_NULL, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_plot = models.IntegerField(blank=True, null=True)
    foreshadowing = models.ManyToManyField('Scene', blank=True)
    scene_location = models.ForeignKey(Location, blank=True, on_delete=models.SET_NULL, null=True)
    characters_present = models.ManyToManyField('CharacterVersion', blank=True)
    scene_summary = models.TextField(blank=True, null=True)
    factions = models.ManyToManyField('Faction', blank=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "for_plot" : self.for_plot.name,
            "order_in_plot": self.order_in_plot,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "scene_location": self.scene_location.to_short_dict(),
            "characters_present": [character_version.to_short_dict() for character_version in self.characters_present.all()],
            "factions": [faction.to_short_dict() for faction in self.factions.all()],
            "scene_summary": self.scene_summary,
        }
    
    def get_brief(self):
        """
        Get a brief description of the instance.
        
        Returns:
            str: A string containing a brief description of the instance.
        """
        brief = f"- Scene: {self.name} \n"
        if self.characters_present.exists(): brief += f"  - Characters present:\n{(character_version.name for character_version in self.characters_present.all())} \n"
        if self.scene_location: brief += f"  - Location: {self.scene_location.name} \n"
        if self.date_from: brief += f"  - From: {self.date_from} \n"
        if self.date_to: brief += f"  - To: {self.date_to} \n"
        if self.scene_summary: brief += f"  - Summary: {self.scene_summary} \n"
        if self.foreshadowing.exists(): brief += f"  - Foreshadowing: {(foreshadowing_scene.name for foreshadowing_scene in self.foreshadowing.all())} \n"
        if self.pacing: brief += f"  - Pacing: {self.pacing.name} \n" 
        
        return brief



class Plot(NovellerModelDecorator):
    plot_for_book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='books_plots', null=True)
    scenes_of_plot = models.ManyToManyField(Scene, blank=True)
    plot_beginning = models.TextField(blank=True, null=True, default="not yet set")
    plot_middle = models.TextField(blank=True, null=True, default="not yet set")
    plot_end = models.TextField(blank=True, null=True, default="not yet set")
    is_sub_plot = models.BooleanField(default=False)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "is_sub_plot": self.is_sub_plot,
            "scenes_of_plot": [scene.to_short_dict() for scene in self.scenes_of_plot.all()],
            "plot_beginning": self.plot_beginning,
            "plot_middle": self.plot_middle,
            "plot_end": self.plot_end,
        }
        
    def get_brief(self):
        """
        Get a brief description of the instance.
        
        Returns:
            str: A string containing a brief description of the instance.
        """
        plot_scenes_to_brief = ""
        if self.scenes_of_plot.exists():
            plot_scenes_to_brief = "- Scenes:\n"
            i = 1
            for plot_scene in self.scenes_of_plot.all():
                plot_scenes_to_brief += f"  {i}: {plot_scene.name} \n"
                i = i + 1
            
        brief = f"{self.name} \n"
        if self.scenes_of_plot.exists(): brief += f"{plot_scenes_to_brief}"
        
        print(colored(f"noveller_models.Plot.get_brief(): brief: {brief}", "yellow"))
        
        return brief
   

class Chapter(NovellerModelDecorator):
    chapter_in_book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='book_characters', null=True)
    chapter_num = models.IntegerField(null=True)
    chapter_goals = models.TextField(blank=True, null=True, default="not yet set")
    chapter_draft_file = models.OneToOneField('File', on_delete=models.SET_NULL, blank=True, null=True)
    parts_for_chapter = models.ManyToManyField('ChapterPart', blank=True, related_name='chapters')
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "chapter_num": self.chapter_num,
            "chapter_goals": self.chapter_goals,
            "parts_for_chapter": [part.to_short_dict() for part in self.parts_for_chapter.all()],
        }
    
    # def __str__(self):
    #     return f"ch.{self.chapter_num}"
    
    class Meta:
        ordering = ['chapter_num']


class ChapterPart(NovellerModelDecorator):
    part_num = models.IntegerField(null=True)
    part_goals = models.TextField(blank=True, null=True, default="not yet set")
    storyteller_of_part = models.OneToOneField('StoryTeller', on_delete=models.SET_NULL, blank=True, null=True)
    themes = models.ManyToManyField('LiteraryTheme', blank=True)
    for_chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, blank=True, null=True, related_name='chapter_parts')
    scene_for_chapter_part = models.ForeignKey('Scene', on_delete=models.SET_NULL, blank=True, null=True, related_name='chapter_parts_for_scene')
    pacing = models.ForeignKey('StoryPacing', blank=True, on_delete=models.SET_NULL, null=True)
    part_breakdown_items = models.ManyToManyField('ChapterPartBreakdownItem', blank=True, related_name='chapter_part_breakdown_items')
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "for_chapter": self.for_chapter.chapter_num,
            "part_num": self.part_num,
            "scene_for_chapter_part": self.scene_for_chapter_part.name,
            "part_goals": self.part_goals,
            "storyteller_of_part": self.storyteller_of_part.name,
            "themes": [theme.name for theme in self.themes.all()],
            "pacing": self.pacing.name,
            "part_breakdown": [part_breakdown_item.to_dict() for part_breakdown_item in self.part_breakdown_items.all()]
        }

    # def __str__(self):
    #     return f"{self.for_chapter}.pt{self.part_num}"
    
    class Meta:
        ordering = ['for_chapter__chapter_num', 'part_num']


class ChapterPartBreakdownItem(NovellerModelDecorator):
    for_chapter_part = models.ForeignKey(ChapterPart, on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField(blank=True)
    order_in_part = models.IntegerField(blank=True, default=0, null=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "order_in_part": self.order_in_part,
            "content": self.content,
        }
    
    # class Meta:
    #     ordering = ['for_chapter_part_summary__for_chapter_part__for_chapter__book','for_chapter_part_summary__for_chapter_part__for_chapter__chapter_num', 'for_chapter_part_summary__for_chapter_part__part_num', 'order_in_part']
    
    
class CharacterRelatedSettingTopic(NovellerModelDecorator):
    character_in_setting = models.ForeignKey('Setting', on_delete=models.SET_NULL, blank=True, null=True)
    rights = models.TextField(blank=True, null=True, default="not yet set")
    appearance_modifiers = models.ForeignKey('CharacterAppearanceModifiers', on_delete=models.SET_NULL, blank=True, null=True)
    attitudes = models.TextField(blank=True, null=True, default="not yet set")
    leisure = models.TextField(blank=True, null=True, default="not yet set")
    food = models.TextField(blank=True, null=True, default="not yet set")
    work = models.TextField(blank=True, null=True, default="not yet set")
    social_life = models.TextField(blank=True, null=True, default="not yet set")
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "character_in_setting": self.character_in_setting.name,
            "rights": self.rights,
            "appearance_modifiers": self.appearance_modifiers.to_dict(),
            "attitudes": self.attitudes,
            "leisure": self.leisure,
            "food": self.food,
            "work": self.work,
            "social_life": self.social_life,
        }
    
    # def __str__(self):
    #     return f"Setting as it relates to {self.character}"


class CharacterTrait(NovellerModelDecorator):
    pass


class CharacterDrive(NovellerModelDecorator):
    pass


class CharacterFear(NovellerModelDecorator):
    pass


class CharacterBelief(NovellerModelDecorator):
    pass
  
    
class CharacterInternalConflict(NovellerModelDecorator):
    pass


class Character(NovellerModelDecorator):
    books = models.ManyToManyField('Book')
    age_at_start = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    sex = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    sexuality = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    origin = models.TextField(blank=True, null=True, default='not yet set')
    representative_of = models.ManyToManyField('LiteraryTheme', blank=True)
    permanent_characteristics = models.TextField(blank=True, null=True, default='not yet set')
    character_versions = models.ManyToManyField('CharacterVersion', blank=True, related_name='version_of_character')
    character_arc = models.TextField(blank=True, null=True, default='not yet set')

    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "age_at_start": self.age_at_start,
            "gender": self.gender,
            "sex": self.sex,
            "sexuality": self.sexuality,
            "origin": self.origin,
            "representative_of": [theme.name for theme in self.representative_of.all()],
            "permanent_characteristics": self.permanent_characteristics,
            "character_versions" : [character_version.to_short_dict() for character_version in self.character_versions.all()], 
            "character_arc": self.character_arc,      
        }


class CharacterVersion(NovellerModelDecorator):
    for_character = models.ForeignKey('Character', blank=True, on_delete=models.SET_NULL, null=True)
    version_num = models.IntegerField(null=True)
    age_at_start = models.IntegerField(blank=True, null=True)
    age_at_end = models.IntegerField(blank=True, null=True)
    locations = models.ManyToManyField('Location', blank=True)
    preferred_weapon = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    appearance = models.ForeignKey('CharacterAppearance', blank=True, on_delete=models.SET_NULL, null=True)
    setting_based_appearance_modifier_options = models.ForeignKey('CharacterAppearanceModifiers', blank=True, on_delete=models.SET_NULL, null=True)
    strengths = models.ManyToManyField('CharacterTrait', related_name='strengths', blank=True)
    weaknesses = models.ManyToManyField('CharacterTrait', related_name='weaknesses', blank=True)
    other_aspects = models.ManyToManyField('CharacterTrait', related_name='other_aspects', blank=True)
    often_perceived_as = models.ManyToManyField('CharacterTrait', related_name='often_perceived_as', blank=True)
    drives = models.ManyToManyField('CharacterDrive', blank=True)
    fears = models.ManyToManyField('CharacterFear', blank=True)
    beliefs = models.ManyToManyField('CharacterBelief', blank=True)
    internal_conflicts = models.ManyToManyField('CharacterInternalConflict', blank=True)
    relationships = models.ManyToManyField('CharacterRelationship', blank=True)
    lit_style_guide = models.ForeignKey('LiteraryStyleGuide', blank=True, null=True, on_delete=models.SET_NULL)


    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "for_character": self.for_character.name,
            "version_num": self.version_num,
            "age_at_start": self.age_at_start,
            "age_at_end": self.age_at_end,
            "locations": [location.name for location in self.locations.all()],
            "preferred_weapon": self.preferred_weapon,
            "character_appearance": self.appearance.to_short_dict(),
            "setting_based_appearance_modifier_options": self.setting_based_appearance_modifier_options.to_dict(),
            "strengths": [strength.name for strength in self.strengths.all()],
            "weaknesses": [weakness.name for weakness in self.weaknesses.all()],
            "other_aspects": [other_aspect.name for other_aspect in self.other_aspects.all()],
            "often_perceived_as": [perceived_as.name for perceived_as in self.often_perceived_as.all()],
            "drives": [drive.name for drive in self.drives.all()],
            "fears": [fear.name for fear in self.fears.all()],
            "beliefs": [belief.name for belief in self.beliefs.all()],
            "internal_conflicts": [internal_conflict.name for internal_conflict in self.internal_conflicts.all()],
            "relationships": [relationship.to_short_dict() for relationship in self.relationships.all()],
            "lit_style_guide": self.lit_style_guide.to_short_dict(),
        }

    # def __str__(self):
    #     return f"{self.for_character} v{self.version_num}"
    
    class Meta:
        ordering = ['for_character__name',]
 
     
class CharacterRelationship(NovellerModelDecorator):
    relationship_from = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, related_name='has_relationship', null=True)
    relationship_to = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, related_name='character_relationship', null=True)
    age_started = models.IntegerField(null=True)
    relationship_descriptors = models.TextField(null=True, default='not yet set')

    def to_short_dict(self):
        return {
            "id": str(self.id),
            "name" : f"The relationship that {self.relationship_from} has towards {self.relationship_to}"
        }

    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : f"The relationship that {self.relationship_from} has towards {self.relationship_to}",
            "relationship_from": self.relationship_from.to_short_dict(),
            "relationship_to": self.relationship_to.to_short_dict(),
            "age_started": self.age_started,
            "relationship_descriptors": self.relationship_descriptors,
        }

    # def __str__(self):
    #     return f"{self.relationship_from}'s relationship with {self.relationship_to}"

    class Meta:
        ordering = ['relationship_from__for_character__name', 'relationship_to__for_character__name']


class CharacterAppearance(NovellerModelDecorator):
    distinguishing_features = models.TextField(null=True, default='not yet set')
    eyes = models.CharField(max_length=200, null=True, default='not yet set')
    hair = models.CharField(max_length=200, null=True, default='not yet set')
    face = models.CharField(max_length=200, null=True, default='not yet set')
    build = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    movement = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    character_version = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, null=True, related_name='appearance_for_character_version')
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : f"the appearance of {self.character_version.name}",
            "distinguishing_features": self.distinguishing_features,
            "eyes": self.eyes,
            "hair": self.hair,
            "face": self.face,
            "build": self.build,
            "movement": self.movement,
        }
        
    # def __str__(self):
    #     return f"{self.character_version}'s appearance"

    class Meta:
        ordering = ['character_version__for_character__name', 'character_version__version_num']


class CharacterAppearanceModifiers(NovellerModelDecorator):
    clothing = models.TextField(blank=True, null=True, default='not yet set')
    hair_head_options = models.TextField(blank=True, null=True, default='not yet set')
    perfume = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    makeup = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    shaving = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    hygiene = models.CharField(max_length=200, blank=True, null=True, default='not yet set')
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "content_type": self.content_type,
            "name" : self.name,
            "clothing": self.clothing,
            "hair_head_options": self.hair_head_options,
            "perfume": self.perfume,
            "makeup": self.makeup,  
            "shaving": self.shaving,
            "hygiene": self.hygiene,
        }
    
    # def __str__(self):
    #     return f"{self.character_version}'s appearance"


class File(NovellerModelDecorator):
    file_location = models.CharField(max_length=255, null=True)
    file_content = models.TextField(blank=True, null=True)

 
# class NovellerModeller(NovellerModelDecorator):
        
#     class __NovellerModellerSingleton:
#         def __init__(self):
#             self.instance = NovellerModeller()
        
#         def __str__(self):
#             return str(self.instance)
        
#         def __getattr__(self, name):
#             return getattr(self.instance, name)
        
#         def __setattr__(self, name):
#             return setattr(self.instance, name)
        
#         def __del__(self):
#             raise TypeError("Singletons can't be deleted")
    
#     _instance = None  # class level variable to hold instance
    
#     @classmethod
#     def get_instance(cls):
#         if not cls._instance:
#             cls._instance = cls.__NovellerModellerSingleton()
#         return cls._instance



class Book(AbstractPhusisProject):
    from_app = models.CharField(max_length=200, default='noveller')
    elaboration = models.TextField(blank=True, null=True)
    settings = models.ManyToManyField(Setting, blank=True, related_name='book_settings')
    plots = models.ManyToManyField(Plot, blank=True, related_name='books_plots')
    chapters = models.ManyToManyField(Chapter, blank=True, related_name='books_chapters')
    characters = models.ManyToManyField(Character, blank=True, related_name='characters_book_characters')
    themes = models.ManyToManyField(LiteraryTheme, blank=True, related_name='book_themes')
    genres = models.ManyToManyField(Genre, blank=True, related_name='book_genres')
    target_audiences = models.ManyToManyField(TargetAudience, blank=True, related_name='book_audiences')
    phusis_applicaton = 'noveller'
    project_type = 'Book'
    
    def project_brief(self):
        """
        Generate a project brief containing various attributes.
        
        Returns:
            str: A string containing the project brief.
        """
        self.project_attributes()
        brief = "# PROJECT BRIEF\n"
        brief += f"## Project Type: {self.project_type}\n"
        brief += f"## Name: {self.name}\n"
        brief += f"## Orchestrator: {self.orchestrator.name}\n"
        
        #GOALS
        if self.goals_for_project.exists():
            brief += f"## Goals:\n"
            for goal in self.goals_for_project.all():
                brief += f"### {goal.name}\n"
                if goal.steps.exists():
                    for step in goal.steps.all():
                        brief += f"- {step.name} \n"
        else: 
            brief += f"## Goals: (not yet set)\n"
        
        #PLOTS
        if self.plots.exists(): 
            brief += f"## Plots:\n"
            for plot in self.plots.all():
                brief += f"### {plot.name}\n"
                if plot.scenes_of_plot.exists():
                    for scene in plot.scenes_of_plot.all():
                        brief += f"- Scene {scene.order_in_plot}: {scene.name} \n"
        else: 
            brief += f"## Plots: (not yet set)\n"


        #CHARACTERS
        if self.characters.exists(): 
            brief += f"## Characters:\n"
            for character in self.characters.all():
                brief += f"### {character.name}\n"
                brief += f"- origin: {character.origin}\n"
                brief += f"- age_at_start: {character.age_at_start}\n"
                brief += f"- gender: {character.gender}\n"
                brief += f"- sexuality: {character.sexuality}\n"
        else: 
            brief += f"## Characters: (not yet set)\n"
       
        #GENRES
        if self.genres.exists(): 
            brief += f"## Genres:\n{convert_array_to_md_list(genre.name for genre in self.genres.all())}"
        else : brief += f"## Genres: (not yet set)\n"

        #SETTINGS
        if self.settings.exists(): 
            brief += f"## Settings:\n{convert_array_to_md_list(setting.name for setting in self.settings.all())}"
        else: brief += f"## Settings: (not yet set)\n"
        
        #THEMES
        if self.themes.exists(): 
            brief += f"## Themes:\n{convert_array_to_md_list(theme.name for theme in self.themes.all())}"
        else: brief += f"## Themes: (not yet set)\n"
        
        #TARGET AUDIENCES
        if self.target_audiences.exists(): 
            brief += f"## Target Audiences:\n{convert_array_to_md_list(audience.name for audience in self.target_audiences.all())}"
        else: brief += f"## Target Audiences: (not yet set)\n"
        
        #ELABORATION
        if self.elaboration: 
            brief += f"## Elaboration:\n- {self.elaboration}"
        else: brief += f"## Elaboration: (not yet set)\n"
        
        return brief
    
    def project_attributes(self):
        """
        Get the project attributes.
        
        Returns:
            list: A list containing the project attributes.
        """
        noveller_app = apps.get_app_config('noveller')
        phusis_project_attribute_subclasses = [
            model for model in noveller_app.get_models()
            if issubclass(model, AbstractPhusisProjectAttribute) and model != AbstractPhusisProjectAttribute
        ]

        project_attributes = []
        for model in phusis_project_attribute_subclasses:
            # print(colored(f"Book.project_attributes: model = {model}", "yellow"))
            # print(colored(f"Book.project_attributes: model.__name__ = {model.__name__}", "yellow"))
            project_attributes.append(model)
 
        return project_attributes
    
    def project_attributes_to_md(self):
        """
        Convert the project attributes to a markdown string.
        
        Returns:
            str: A markdown string containing the project attributes.
        """
        atts = self.project_attributes()
        atts_to_md = ""
        for attribute in atts:
            # print(colored(f"Book.project_attributes_to_md: model = {attribute}", "yellow"))
            atts_to_md = atts_to_md + f"- {attribute.__name__}\n"
       
        return atts_to_md
    
    def list_project_attributes(self):
        """
        List the project attributes and their sub-attributes.
        
        Returns:
            tuple: A tuple containing a dictionary of the project attributes and a string representation.
        """
        book_attributes_str = f"These are the various attributes, and their sub attributes of {self.name}:\n"
        models_dict = {}
        app_models = self.project_attributes()
        for model in app_models:
            model_name = model.__name__
            fields = [field.name for field in model._meta.fields]
            models_dict[model_name] = fields
        
        for model, fields in models_dict.items():
            book_attributes_str += f"Attribute: {model}\n"
        
        return models_dict, book_attributes_str
    
    def set_data(self, properties_dict):
        """
        Set the data for the instance based on the provided properties dictionary.
        
        Args:
            properties_dict (dict): A dictionary containing the properties to set for the instance.
        """
        self.project_attributes()
        for key, value in properties_dict.items():
            # Get the field instance
            field = self._meta.get_field(key)

            if isinstance(field, models.ManyToManyField):
                related_objects = []

                # Find the related objects using find_attribute_by function
                for attr_name in value:
                    # print(colored(f"Book.set_data(): {field.related_model} {attr_name}", "green"))
                    attr_clas, attr_instance = find_and_update_or_create_attribute_by(attr_name, field.related_model)
                    related_objects.append(attr_instance)

                # Set the related objects to the attribute
                getattr(self, key).set(related_objects)
            else:
                # Handle other attribute types as needed
                setattr(self, key, value)
        self.save()  
    
    
def convert_array_to_md_list(array):
    """
    Convert an array of items to a markdown list.
    
    Args:
        array (list): A list of items to convert to a markdown list.
    
    Returns:
        str: A markdown string containing the list items.
    """
    items_to_md = ""
    for item in array:
        items_to_md = items_to_md + f"- {item}\n"
    
    return items_to_md

def load_model_and_return_instance_from(json_data, app_name):
    """
    Load a model for the noveller app as JSON dict and return an instance based on the provided JSON data.
    
    Args:
        json_data (dict): A dictionary containing the JSON data for the Noveller model.
    
    Returns:
        object: An instance of the Noveller model created or updated based on the JSON data.
    """
    from phusis.phusis_utils import is_valid_init_json
    from termcolor import colored
    
    new_noveller_obj = {}
    expected_json = {
        "class_name": "NovellorClassName",
        "properties": {
            "name": "Instance Name"
        }
    }
 
    if is_valid_init_json(json_data):
        model_class = {}
        if json_data['class_name'] in globals():
            model_class = apps.get_model("noveller", f"{json_data['class_name']}")
        else: 
            # print(colored(f"noveller_models.create_project_model_from_instance: class_name {json_data['class_name']} not found in globals()", "yellow"))
            pass


        print(colored(f"noveller_models.create_project_model_from_instance: model_class {model_class}. json_data['properties']['name'] {json_data['properties']['name']}", "green"))

        new_noveller_obj, created = model_class.objects.update_or_create(name=json_data['properties']['name'])

        new_noveller_obj.set_data(json_data['properties'])
        new_noveller_obj.save()
        s = f"found and updated with:\n{json_data['properties']}"
        if created: s = "created"
        # print(colored(f"load_noveller_model_and_return_instance_from: {new_noveller_obj.name} {s}", "green"))
        
    else:
        print(colored(f"noveller_models.create_project_model_from_instance: JSON data for agent not valid, expected schema below","red"))
        print(colored(f"Data received: {json_data}", "red"))
        print(colored(f"Minimum expected: {expected_json}", "yellow"))

    return new_noveller_obj

def find_and_update_or_create_attribute_by(attr_name, model_class):
    """
    Args:
        attr_name (str): The name of the attribute to find or create.
        model_class (class): The model class to search for the attribute in.

    Returns:
        tuple: A tuple containing the attribute class and the attribute instance.
    """

    # print(colored(f"noveller_models.find_and_update_or_create_attribute_by(): attr_name: {attr_name}\nmodel_class : {model_class}", "yellow"))
    
    # Check if the attribute exists in the model class
    if hasattr(model_class, attr_name):
        return model_class, getattr(model_class, attr_name)

    # print(colored(f"model class : {model_class}", "yellow"))

    # Check if the attribute exists in any related models
    for related_object in model_class._meta.related_objects:
        related_model_class = related_object.related_model

        if hasattr(related_model_class, attr_name):
            # Create an instance of the related model to return
            instance = related_model_class.objects.get(**{related_object.field.name: model_class})
            return related_model_class, instance
        else:
            #If the Attribute wasn't found, create it 
            new_attribute, created = model_class.objects.update_or_create(name=attr_name)
            return related_model_class, new_attribute
