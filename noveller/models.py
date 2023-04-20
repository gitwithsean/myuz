from __future__ import annotations
from django.db import models
from django.contrib.contenttypes.models import ContentType
from phusis.models import AbstractPhusisProject, AgentBookRelationship
import uuid

class NovellerModelDecorator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)  
    elaboration = models.TextField(blank=True, null=True)
    expose_rest = True
    
    class Meta:
        abstract = True
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Book(AbstractPhusisProject):
    elaboration = models.TextField(blank=True, null=True)
    settings = models.ManyToManyField('Setting', blank=True, related_name='book_settings')
    plot = models.ManyToManyField('PlotEvent', blank=True, related_name='books_events')
    chapters = models.ManyToManyField('Chapter', blank=True, related_name='books_chapters')
    characters = models.ManyToManyField('Character', blank=True, related_name='characters_book_characters')
    themes = models.ManyToManyField('Theme', blank=True, related_name='book_themes')
    genre = models.ManyToManyField('Genre', blank=True, related_name='book_genres')
    target_audiences = models.ManyToManyField('TargetAudience', blank=True, related_name='book_audiences')  
    expose_rest = models.BooleanField(default=True)
    agents_for_project = models.ManyToManyField(
        ContentType,
        related_name="projects_assigned_to",
        through=AgentBookRelationship,
        limit_choices_to=models.Q(app_label='phusis', model='characteragent') |
                         models.Q(app_label='phusis', model='poeticsagent') |
                         models.Q(app_label='phusis', model='writingagent') |
                         models.Q(app_label='phusis', model='researchagent')
    )
    
    # def add_agent_for_book(self, agent):
    #     AgentBookRelationship(agent=agent, book=self)
    
    # def agents_for_book(self):
    #     self.agents_for_project.all()
    
class Genre(NovellerModelDecorator):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='books_genres')
    genre_combos = models.TextField(blank=True, null=True)
    
class TargetAudience(NovellerModelDecorator):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='books_audience')

class Plot(NovellerModelDecorator):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='books_plots')
    events_of_plot = models.ManyToManyField('PlotEvent', blank=True)
        
class PlotEvent(NovellerModelDecorator):
    subplot_of = models.ForeignKey('Plot', on_delete=models.CASCADE, related_name='plots_events', null=True)
    description = models.TextField(blank=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_story_events = models.IntegerField(blank=True, null=True)
    order_in_narrative_telling = models.IntegerField(blank=True, null=True)
    foreshadowing = models.ManyToManyField('PlotEvent', 'SubPlotEvent', blank=True)
    is_climax_of_plot = models.BooleanField(blank=True, null=True)

class SubPlot(Plot):
    sub_plot_of = models.ForeignKey('Plot', on_delete=models.CASCADE, related_name='plots_subplot')
    events_of_subplot = models.ManyToManyField('SubPlotEvent', blank=True, related_name='subplots_events')
    
    class Meta:
        ordering = ['sub_plot_of__name', 'name']

class SubPlotEvent(PlotEvent):
    subplot = models.ForeignKey('SubPlot', on_delete=models.CASCADE, related_name='subplots_events', null=True)
    
    def __str__(self):
        return f"Story Event {self.order_in_story_events}: {self.description}"
    
    class Meta:
        ordering = ['order_in_story_events']

#Chapters, Outlines, Summaries
class Chapter(NovellerModelDecorator):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='book_characters')
    chapter_num = models.IntegerField()
    chapter_title = models.CharField(max_length=200, blank=True)
    chapter_goals = models.TextField(blank=True, null=True)
    chapter_file = models.OneToOneField('File', on_delete=models.SET_NULL, blank=True, null=True)
    parts_for_chapter = models.ManyToManyField('ChapterPart', blank=True, related_name='chapters')
    
    def __str__(self):
        return f"ch.{self.chapter_num}"
    
    class Meta:
        ordering = ['chapter_num']

class ChapterPart(NovellerModelDecorator):
    part_title = models.CharField(max_length=200, blank=True)
    part_num = models.IntegerField()
    part_goals = models.TextField(blank=True, null=True)
    teller = models.OneToOneField('StoryTeller', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ManyToManyField('Location', blank=True)
    chapter = models.ForeignKey('Chapter', on_delete=models.SET_NULL, blank=True, null=True)
    characters = models.ManyToManyField('CharacterVersion', blank=True)
    themes = models.ManyToManyField('Theme', blank=True)
    factions = models.ManyToManyField('Faction', blank=True)
    chapter_part_summary = models.ManyToManyField('ChapterPartSummary', blank=True)
    for_chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, blank=True, null=True, related_name='chapter_parts')

    def __str__(self):
        return f"{self.chapter}.pt{self.part_num}"
    
    class Meta:
        ordering = ['chapter__chapter_num', 'part_num']

class ChapterPartSummary(NovellerModelDecorator):
    for_chapter_part = models.OneToOneField('ChapterPart', on_delete=models.SET_NULL, blank=True, null=True)
    chapter_summary = models.TextField(blank=True)
    themes = models.ManyToManyField('Theme', blank=True)
    pacing = models.ManyToManyField('Pacing', blank=True,)
    summary_items = models.ForeignKey('ChapterPartSummaryItem', on_delete=models.SET_NULL, blank=True, null=True, related_name='chapter_part_summary')
    summary_items = models.ManyToManyField('ChapterPartSummaryItem', related_name='chapter_part_summary_items')
    
    def __str__(self):
        return f"{self.for_chapter_part}"
    
    class Meta:
        ordering = ['for_chapter_part__chapter__chapter_num', 'for_chapter_part__part_num']

class ChapterPartSummaryItem(NovellerModelDecorator):
    for_chapter_part = models.ForeignKey('ChapterPartSummary', on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField(blank=True)
    order_in_part = models.IntegerField(blank=True, default=0)
    
    def __str__(self):
        return f"{self.for_chapter_part}-{self.order_in_part}: {self.content}"
    
    class Meta:
        ordering = ['for_chapter_part__for_chapter_part__chapter__book','for_chapter_part__for_chapter_part__chapter__chapter_num', 'for_chapter_part__for_chapter_part__part_num', 'order_in_part']

class Pacing(NovellerModelDecorator):
    pass
    
# Background, Setting and Research

class Setting(NovellerModelDecorator):
    books = models.ManyToManyField('Book', blank=True)
    bg_events = models.ManyToManyField('BGEvent', blank=True)
    factions = models.ManyToManyField('Faction', blank=True)
    bg_research = models.OneToOneField('BGResearch', on_delete=models.SET_NULL, blank=True, null=True)
    general_setting = models.TextField(blank=True)

class Location(NovellerModelDecorator):
    character_versions = models.ManyToManyField('CharacterVersion', blank=True, related_name='locations_in_character_version')

class BGResearch(NovellerModelDecorator):
    bg_research = models.TextField(blank=True)
    deeper_bg_research_topic = models.ManyToManyField('DeeperBGResearchTopic', blank=True)
    
class DeeperBGResearchTopic(NovellerModelDecorator):
    notes = models.TextField(blank=True)

class BGEvent(NovellerModelDecorator):
    event = models.CharField(max_length=200)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_story_events = models.IntegerField(blank=True, null=True)
    order_in_narrative_telling = models.IntegerField(blank=True, null=True)

class Faction(NovellerModelDecorator):
    description = models.TextField(blank=True)
    members = models.ManyToManyField('CharacterVersion', blank=True)
    
class CharacterRelatedSettingTopic(NovellerModelDecorator):
    setting = models.ForeignKey('Setting', on_delete=models.SET_NULL, blank=True, null=True)
    character = models.ForeignKey('CharacterVersion', on_delete=models.SET_NULL, blank=True, null=True)
    rights = models.TextField(blank=True, null=True)
    appearance_modifiers = models.ForeignKey('AppearanceModifiers', on_delete=models.SET_NULL, blank=True, null=True)
    attitudes = models.TextField(blank=True, null=True)
    leisure = models.TextField(blank=True, null=True)
    food = models.TextField(blank=True, null=True)
    work = models.TextField(blank=True, null=True)
    social_life = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Setting as it relates to {self.character}"

class Character(NovellerModelDecorator):
    book = models.ManyToManyField('Book')
    age_at_start = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=200, blank=True, null=True)
    sex = models.CharField(max_length=200, blank=True, null=True)
    sexuality = models.CharField(max_length=200, blank=True, null=True)
    origin = models.TextField(blank=True, null=True)
    representative_of = models.ManyToManyField('Theme', blank=True)
    permanent_characteristics = models.TextField(blank=True, null=True)
    versions = models.ManyToManyField('CharacterVersion', blank=True, related_name='+')
    character_arc = models.TextField(blank=True, null=True)

class CharacterVersion(NovellerModelDecorator):
    for_character = models.ForeignKey('Character', blank=True, on_delete=models.SET_NULL, null=True)
    version_num = models.IntegerField()
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
    relationship_for = models.OneToOneField('CharacterRelationship', blank=True, on_delete=models.SET_NULL, null=True, related_name='+')
    relationship_with = models.OneToOneField('CharacterRelationship', blank=True, on_delete=models.SET_NULL, null=True, related_name='+')
    subter = models.CharField(max_length=200, blank=True, null=True)
    lit_style_guides = models.ForeignKey('LitStyleGuide', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.for_character} v{self.version_num}"
    
    class Meta:
        ordering = ['for_character__name',]
     
class CharacterRelationship(NovellerModelDecorator):
    relationship_from = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, related_name='has_relationship')
    relationship_to = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, related_name='character_relationship')
    age_started = models.IntegerField()
    relationship_descriptors = models.TextField()
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE, null=True, related_name='character_versions')
    
    def __str__(self):
        return f"{self.character_version}'s relationship with {self.relationship_to}"

    class Meta:
        ordering = ['relationship_from__for_character__name', 'relationship_to__for_character__name']

class Appearance(NovellerModelDecorator):
    distinguishing_features = models.TextField()
    eyes = models.CharField(max_length=200)
    hair = models.CharField(max_length=200)
    face = models.CharField(max_length=200)
    build = models.CharField(max_length=200, blank=True, null=True)
    movement = models.CharField(max_length=200, blank=True, null=True)
    character_version = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, null=True, related_name='appearance_for_character_version')

    def __str__(self):
        return f"{self.character_version}'s appearance"

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
    
    def __str__(self):
        return f"{self.character_version}'s appearance"

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
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.SET_NULL, blank=True, null=True)
    perspective = models.ForeignKey('Perspective', on_delete=models.CASCADE)
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
    person = models.CharField(max_length=200)
    sources = models.ManyToManyField('LiteraryInspirationSource', blank=True)

class LiteraryInspirationSource(NovellerModelDecorator):
    source = models.CharField(max_length=200)

class StoryTeller(NovellerModelDecorator):
    character = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE)
    style = models.ForeignKey('LitStyleGuide', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.character} style as a story teller"
    
    class Meta:
        ordering = ['character__for_character__name']

class Theme(NovellerModelDecorator):
    pass

class Perspective(NovellerModelDecorator):
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
    file_location = models.CharField(max_length=255)
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
