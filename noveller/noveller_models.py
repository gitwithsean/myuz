from __future__ import annotations
from django.db import models
from django.contrib.contenttypes.models import ContentType
from phusis.agent_models import AbstractPhusisProject, AgentBookRelationship
import uuid
from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint
from rest_framework import serializers
from django.apps import apps

class NovellerModelDecorator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)  
    elaboration = models.TextField(blank=True, null=True)
    expose_rest = True
    
    class Meta:
        abstract = True
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def set_name():
        pass
    
    # NovellerModelDecorator set_data
    def set_data(self, properties_dict):
        pprint(properties_dict)
        for key, value in properties_dict.items():
            # Get the field instance
            field = self._meta.get_field(key)
            # print(f"key: {key}\nvalue: {value}\nfield: {field}\n")
            if isinstance(field, models.ManyToManyField):
                related_objects = []
                # print(f"key: {key}\nvalue: {value}\nfield: {field}\n")
                # Find the related objects using find_attribute_by function
                for attr_name in value:
                    # print(f"{field.related_model} {attr_name}")
                    attr_clas, attr_instance = find_and_update_or_create_attribute_by(attr_name, field.related_model)
                    related_objects.append(attr_instance)

                # Set the related objects to the attribute
                getattr(self, key).set(related_objects)
            elif isinstance(field, models.ForeignKey):
                attr_clas, attr_instance = find_and_update_or_create_attribute_by(value, field.related_model)
                setattr(self, key, attr_instance)
            else:
                # Handle other attribute types as needed
                
                print(f"key: {key}\nvalue: {value}\nfield: {field}\n")
                setattr(self, key, value)
        self.save()        
        

class Genre(NovellerModelDecorator):
    pass

    
class TargetAudience(NovellerModelDecorator):
    pass

class Plot(NovellerModelDecorator):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='books_plots', null=True)
    events_of_plot = models.ManyToManyField('PlotEvent', blank=True)
        
class PlotEvent(NovellerModelDecorator):
    for_plot = models.ForeignKey('Plot', on_delete=models.CASCADE, related_name='plots_events', null=True)
    description = models.TextField(blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_story_events = models.IntegerField(blank=True, null=True)
    order_in_narrative_telling = models.IntegerField(blank=True, null=True)
    foreshadowing = models.ManyToManyField('PlotEvent', 'SubPlotEvent', blank=True)
    is_climax_of_plot = models.BooleanField(blank=True, null=True)

class SubPlot(Plot):
    sub_plot_of = models.ForeignKey('Plot', on_delete=models.CASCADE, related_name='plots_subplot', null=True)
    events_of_subplot = models.ManyToManyField('SubPlotEvent', blank=True, related_name='subplots_events')
    
    class Meta:
        ordering = ['sub_plot_of__name', 'name']

class SubPlotEvent(PlotEvent):
    subplot = models.ForeignKey('SubPlot', on_delete=models.CASCADE, related_name='subplots_events', null=True)
    
    # def __str__(self):
    #     return f"Story Event {self.order_in_story_events}: {self.description}"
    
    class Meta:
        ordering = ['order_in_story_events']

#Chapters, Outlines, Summaries
class Chapter(NovellerModelDecorator):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='book_characters', null=True)
    chapter_num = models.IntegerField(null=True)
    chapter_goals = models.TextField(blank=True, null=True)
    chapter_draft_file = models.OneToOneField('File', on_delete=models.SET_NULL, blank=True, null=True)
    parts_for_chapter = models.ManyToManyField('ChapterPart', blank=True, related_name='chapters')
    
    # def __str__(self):
    #     return f"ch.{self.chapter_num}"
    
    class Meta:
        ordering = ['chapter_num']

class ChapterPart(NovellerModelDecorator):
    part_num = models.IntegerField(null=True)
    part_goals = models.TextField(blank=True, null=True)
    storyteller = models.OneToOneField('StoryTeller', on_delete=models.SET_NULL, blank=True, null=True)
    locations = models.ManyToManyField('Location', blank=True)
    character_versions = models.ManyToManyField('CharacterVersion', blank=True)
    themes = models.ManyToManyField('LiteraryTheme', blank=True)
    factions = models.ManyToManyField('Faction', blank=True)
    chapter_part_summary = models.ManyToManyField('ChapterPartSummary', blank=True)
    for_chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, blank=True, null=True, related_name='chapter_parts')

    # def __str__(self):
    #     return f"{self.for_chapter}.pt{self.part_num}"
    
    class Meta:
        ordering = ['for_chapter__chapter_num', 'part_num']

class ChapterPartSummary(NovellerModelDecorator):
    for_chapter_part = models.OneToOneField('ChapterPart', on_delete=models.SET_NULL, blank=True, null=True)
    chapter_part_summary = models.TextField(blank=True, null=True)
    themes = models.ManyToManyField('LiteraryTheme', blank=True)
    pacing = models.ManyToManyField('Pacing', blank=True)
    part_summary_items = models.ManyToManyField('ChapterPartSummaryItem', blank=True, related_name='chapter_part_summary_items')
    
    # def __str__(self):
    #     return f"{self.for_chapter_part}"
    
    class Meta:
        ordering = ['for_chapter_part__for_chapter__chapter_num', 'for_chapter_part__part_num']

class ChapterPartSummaryItem(NovellerModelDecorator):
    for_chapter_part_summary = models.ForeignKey('ChapterPartSummary', on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField(blank=True)
    order_in_part = models.IntegerField(blank=True, default=0, null=True)
    
    # def __str__(self):
    #     return f"{self.for_chapter_part_summary}-{self.order_in_part}: {self.content}"
    
    class Meta:
        ordering = ['for_chapter_part_summary__for_chapter_part__for_chapter__book','for_chapter_part_summary__for_chapter_part__for_chapter__chapter_num', 'for_chapter_part_summary__for_chapter_part__part_num', 'order_in_part']

class Pacing(NovellerModelDecorator):
    pass
    
# Background, Setting and Research

class Setting(NovellerModelDecorator):
    books = models.ManyToManyField('Book', blank=True)
    background_events = models.ManyToManyField('BackgroundEvent', blank=True)
    factions = models.ManyToManyField('Faction', blank=True)
    background_research = models.OneToOneField('BackgroundResearch', on_delete=models.SET_NULL, blank=True, null=True)
    general_setting = models.TextField(blank=True)

class Location(NovellerModelDecorator):
    character_versions = models.ManyToManyField('CharacterVersion', blank=True, related_name='locations_in_character_version')

class BackgroundResearch(NovellerModelDecorator):
    research = models.TextField(blank=True)
    deeper_research_topics = models.ManyToManyField('DeeperBackgroundResearchTopic', blank=True)
    
class DeeperBackgroundResearchTopic(NovellerModelDecorator):
    notes = models.TextField(blank=True, null=True)

class BackgroundEvent(NovellerModelDecorator):
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_story_events = models.IntegerField(blank=True, null=True)
    order_in_narrative_telling = models.IntegerField(blank=True, null=True)

class Faction(NovellerModelDecorator):
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField('CharacterVersion', blank=True)
    
class CharacterRelatedSettingTopic(NovellerModelDecorator):
    setting = models.ForeignKey('Setting', on_delete=models.SET_NULL, blank=True, null=True)
    rights = models.TextField(blank=True, null=True)
    appearance_modifiers = models.ForeignKey('AppearanceModifiers', on_delete=models.SET_NULL, blank=True, null=True)
    attitudes = models.TextField(blank=True, null=True)
    leisure = models.TextField(blank=True, null=True)
    food = models.TextField(blank=True, null=True)
    work = models.TextField(blank=True, null=True)
    social_life = models.TextField(blank=True, null=True)
    
    # def __str__(self):
    #     return f"Setting as it relates to {self.character}"

class Character(NovellerModelDecorator):
    books = models.ManyToManyField('Book')
    age_at_start = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=200, blank=True, null=True)
    sex = models.CharField(max_length=200, blank=True, null=True)
    sexuality = models.CharField(max_length=200, blank=True, null=True)
    origin = models.TextField(blank=True, null=True)
    representative_of = models.ManyToManyField('LiteraryTheme', blank=True)
    permanent_characteristics = models.TextField(blank=True, null=True)
    versions = models.ManyToManyField('CharacterVersion', blank=True, related_name='version_of_character')
    character_arc = models.TextField(blank=True, null=True)

class CharacterVersion(NovellerModelDecorator):
    for_character = models.ForeignKey('Character', blank=True, on_delete=models.SET_NULL, null=True)
    version_num = models.IntegerField(null=True)
    age_at_start = models.IntegerField(blank=True, null=True)
    age_at_end = models.IntegerField(blank=True, null=True)
    locations = models.ManyToManyField('Location', blank=True)
    preferred_weapon = models.CharField(max_length=200, blank=True, null=True)
    appearance = models.ForeignKey('Appearance', blank=True, on_delete=models.SET_NULL, null=True)
    setting_based_appearance_modifier_options = models.ForeignKey('AppearanceModifiers', blank=True, on_delete=models.SET_NULL, null=True)
    strengths = models.ManyToManyField('CharacterTrait', related_name='strengths', blank=True)
    weaknesses = models.ManyToManyField('CharacterTrait', related_name='weaknesses', blank=True)
    other_aspects = models.ManyToManyField('CharacterTrait', related_name='other_aspects', blank=True)
    often_perceived_as = models.ManyToManyField('CharacterTrait', related_name='often_perceived_as', blank=True)
    drives = models.ManyToManyField('Drive', blank=True)
    fears = models.ManyToManyField('Fear', blank=True)
    beliefs = models.ManyToManyField('Belief', blank=True)
    internal_conflicts = models.ManyToManyField('InternalConflict', blank=True)
    relationships = models.OneToOneField('CharacterRelationship', blank=True, on_delete=models.SET_NULL, null=True)
    subter = models.CharField(max_length=200, blank=True, null=True)
    lit_style_guide = models.ForeignKey('LitStyleGuide', blank=True, null=True, on_delete=models.SET_NULL)

    # def __str__(self):
    #     return f"{self.for_character} v{self.version_num}"
    
    class Meta:
        ordering = ['for_character__name',]
 
     
class CharacterRelationship(NovellerModelDecorator):
    relationship_from = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, related_name='has_relationship', null=True)
    relationship_to = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, related_name='character_relationship', null=True)
    age_started = models.IntegerField(null=True)
    relationship_descriptors = models.TextField(null=True)
    
    # def __str__(self):
    #     return f"{self.relationship_from}'s relationship with {self.relationship_to}"

    class Meta:
        ordering = ['relationship_from__for_character__name', 'relationship_to__for_character__name']


class Appearance(NovellerModelDecorator):
    distinguishing_features = models.TextField(null=True)
    eyes = models.CharField(max_length=200, null=True)
    hair = models.CharField(max_length=200, null=True)
    face = models.CharField(max_length=200, null=True)
    build = models.CharField(max_length=200, blank=True, null=True)
    movement = models.CharField(max_length=200, blank=True, null=True)
    character_version = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, null=True, related_name='appearance_for_character_version')

    # def __str__(self):
    #     return f"{self.character_version}'s appearance"

    class Meta:
        ordering = ['character_version__for_character__name', 'character_version__version_num']


class AppearanceModifiers(NovellerModelDecorator):
    clothing = models.TextField(blank=True, null=True)
    hair_head_options = models.TextField(blank=True, null=True)
    perfume = models.CharField(max_length=200, blank=True, null=True)
    makeup = models.CharField(max_length=200, blank=True, null=True)
    shaving = models.CharField(max_length=200, blank=True, null=True)
    hygiene = models.CharField(max_length=200, blank=True, null=True)
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE, null=True)
    
    # def __str__(self):
    #     return f"{self.character_version}'s appearance"

    class Meta:
        ordering = ['character_version__for_character__name', 'character_version__version_num']


class CharacterTrait(NovellerModelDecorator):
    pass


class Drive(NovellerModelDecorator):
    pass


class Fear(NovellerModelDecorator):
    pass


class Belief(NovellerModelDecorator):
    pass
  
    
class InternalConflict(NovellerModelDecorator):
    pass


class LitStyleGuide(NovellerModelDecorator):
    perspective = models.ForeignKey('NarrativePerspective', on_delete=models.CASCADE, null=True)
    inspirations = models.ManyToManyField('LiteraryInspirationPerson', blank=True)
    tone = models.ManyToManyField('LiteraryTone', blank=True)
    imagery = models.ManyToManyField('LiteraryImagery', blank=True)
    symbolism = models.ManyToManyField('LiterarySymbolism', blank=True)
    traits = models.ManyToManyField('LiteraryTrait', related_name='litstyleguide_traits', blank=True)
    avoid = models.ManyToManyField('LiteraryTrait', related_name='litstyleguide_avoid', blank=True)
    style_guide = models.TextField(blank=True, null=True)
    compressed_sg = models.TextField(blank=True, null=True)
    writing_samples = models.TextField(blank=True, null=True)


class LiteraryInspirationPerson(NovellerModelDecorator):
    sources = models.ManyToManyField('LiteraryInspirationSource', blank=True)


class LiteraryInspirationSource(NovellerModelDecorator):
    pass

class StoryTeller(NovellerModelDecorator):
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE, null=True)
    lit_style_guide = models.ForeignKey('LitStyleGuide', on_delete=models.CASCADE, null=True)
    
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

# Other
class File(NovellerModelDecorator):
    file_location = models.CharField(max_length=255, null=True)
    file_content = models.TextField(blank=True, null=True)
    expose_rest = False

 
class NovellerModellor(NovellerModelDecorator):
        
    class __NovellerModellorSingleton:
        def __init__(self):
            self.instance = NovellerModellor()
        
        def __str__(self):
            return str(self.instance)
        
        def __getattr__(self, name):
            return getattr(self.instance, name)
        
        def __setattr__(self, name):
            return setattr(self.instance, name)
        
        def __del__(self):
            raise TypeError("Singletons can't be deleted")
    
    _instance = None  # class level variable to hold instance
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__NovellerModellorSingleton()
        return cls._instance



class Book(AbstractPhusisProject):
    from_app = models.CharField(max_length=200, default='noveller')
    elaboration = models.TextField(blank=True, null=True)
    settings = models.ManyToManyField(Setting, blank=True, related_name='book_settings')
    plots = models.ManyToManyField(Plot, blank=True, related_name='books_events')
    chapters = models.ManyToManyField(Chapter, blank=True, related_name='books_chapters')
    characters = models.ManyToManyField(Character, blank=True, related_name='characters_book_characters')
    themes = models.ManyToManyField(LiteraryTheme, blank=True, related_name='book_themes')
    genres = models.ManyToManyField(Genre, blank=True, related_name='book_genres')
    target_audiences = models.ManyToManyField(TargetAudience, blank=True, related_name='book_audiences')  
    expose_rest = models.BooleanField(default=True)
    agents_for_project = models.ManyToManyField(
        ContentType,
        related_name="projects_assigned_to",
        through=AgentBookRelationship,
        # limit_choices_to=models.Q(app_label='phusis', model='characteragent') |
        #                  models.Q(app_label='phusis', model='poeticsagent') |
        #                  models.Q(app_label='phusis', model='writingagent') |
        #                  models.Q(app_label='phusis', model='researchagent')
    )
    
    def add_agents_to(self, agents):
        for agent in agents:
            agent_content_type = ContentType.objects.get_for_model(agent)
            relationship, created= AgentBookRelationship.objects.get_or_create(content_type=agent_content_type, object_id=agent.id, book=self)
            relationship.save()
            self.save()
            agent.save()
        
        print("SHOWING AGENTS JUST ASSIGNED TO BOOK")
        pprint(self.get_agents_for())    
            
    def get_agents_for(self):
        agent_relationships = AgentBookRelationship.objects.filter(book=self)
        agents = []

        for relationship in agent_relationships:
            agent_content_type = relationship.content_type
            agent_object_id = relationship.object_id
            try:
                agent = agent_content_type.get_object_for_this_type(pk=agent_object_id)
                agents.append(agent)
            except ObjectDoesNotExist:
                print(f"Warning: Agent with content_type={agent_content_type} and object_id={agent_object_id} not found")

        return agents

    def to_dict(self):
        return {
            "name": self.name,
            "project_type": self.project_type,
            "project_workspace": self.project_workspace,
            "agents_for_project": self.get_agents_for()
        }
    
    def list_project_attributes(self):
        book_attributes_str = f"These are the various attributes, and their sub attributes of {self.name}:\n"
        attributes = dir(self)
        models_dict = {}
        app_models = apps.get_app_config('noveller').get_models()
        for model in app_models:
            model_name = model.__name__
            fields = [field.name for field in model._meta.fields]
            models_dict[model_name] = fields
        
        for model, fields in models_dict.items():
            book_attributes_str += f"Model: {model}\n"
            book_attributes_str += "Fields:\n"
        for field in fields:
            book_attributes_str += f"  - {field}\n"
            book_attributes_str += "\n"
        
        return models_dict, book_attributes_str

    def get_project_details(self, to='assess'):
        details=self.project_user_input
        #TODO: Add in the rest of the project details
        return details
    
    def set_data(self, properties_dict):
        for key, value in properties_dict.items():
            # Get the field instance
            field = self._meta.get_field(key)

            if isinstance(field, models.ManyToManyField):
                related_objects = []

                # Find the related objects using find_attribute_by function
                for attr_name in value:
                    print(f"{field.related_model} {attr_name}")
                    attr_clas, attr_instance = find_and_update_or_create_attribute_by(attr_name, field.related_model)
                    related_objects.append(attr_instance)

                # Set the related objects to the attribute
                getattr(self, key).set(related_objects)
            else:
                # Handle other attribute types as needed
                setattr(self, key, value)
        self.save()  
                
# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__' 
        
# def serialize(obj):
#     instance = Book.objects.first()
#     serializer = BookSerializer(instance)
    



def load_noveller_model_and_return_instance_from(json_data):
    from phusis.agent_utils import is_valid_init_json
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
            print(colored(f"noveller_models.create_noveller_model_from_instance: class_name {json_data['class_name']} not found in globals()", "red"))

        new_noveller_obj, created = model_class.objects.update_or_create(name=json_data['properties']['name'])

        new_noveller_obj.set_data(json_data['properties'])
        new_noveller_obj.save()
        s = f"found and updated with:\n{json_data['properties']}"
        if created: s = "created"
        print(colored(f"load_noveller_model_and_return_instance_from: {new_noveller_obj.name} {s}", "green"))
        
    else:
        print(colored(f"models.create_agent_model_from_instance: JSON data for agent not valid, expected schema below","red"))
        print(colored(f"Data received: {json_data}", "red"))
        print(colored(f"Minimum expected: {expected_json}", "yellow"))

    return new_noveller_obj


def find_and_update_or_create_attribute_by(attr_name, model_class):

    # print(f"find_attribute_by(): attr_name: {attr_name}\nmodel_class : {model_class}")
    
    # Check if the attribute exists in the model class
    if hasattr(model_class, attr_name):
        return model_class, getattr(model_class, attr_name)

    # print(f"model class : {model_class}")

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
