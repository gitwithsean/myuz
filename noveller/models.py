from __future__ import annotations
from django.db import models
import uuid
from django.apps import apps

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    settings = models.ManyToManyField('Setting', blank=True, related_name='book_settings')
    events = models.ManyToManyField('StoryEvent', blank=True, null=True, related_name='books_events')
    chapters = models.ManyToManyField('Chapter', blank=True, null=True, related_name='books_chapters')
    characters = models.ManyToManyField('Character', blank=True, null=True, related_name='characters_book_characters')
    
    def __str__(self):
        return self.name

class StoryEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='books_story_events')
    description = models.TextField(blank=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_story_events = models.IntegerField(blank=True, null=True)
    order_in_narrative_telling = models.IntegerField(blank=True, null=True)
        
    def __str__(self):
        return f"Story Event {self.order_in_story_events}: {self.description}"

#Chapters, Outlines, Summaries
class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    books = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='book_characters')
    chapter_num = models.IntegerField()
    chapter_title = models.CharField(max_length=200, blank=True)
    chapter_file = models.OneToOneField('File', on_delete=models.SET_NULL, blank=True, null=True)
    parts_for_chapter = models.ManyToManyField('ChapterPart', blank=True, null=True,  related_name='chapters')
    
    def __str__(self):
        return f"ch.{self.chapter_num}"


class ChapterPart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    part_title = models.CharField(max_length=200, blank=True)
    part_num = models.IntegerField()
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

class ChapterPartSummary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200, blank=True)
    for_chapter_part = models.OneToOneField('ChapterPart', on_delete=models.SET_NULL, blank=True, null=True)
    chapter_summary = models.TextField(blank=True)
    themes = models.ManyToManyField('Theme', blank=True)
    summary_items = models.ForeignKey('ChapterPartSummaryItem', on_delete=models.SET_NULL, blank=True, null=True, related_name='chapter_part_summary')
    summary_items = models.ManyToManyField('ChapterPartSummaryItem', related_name='chapter_part_summary_items')

    def __str__(self):
        return f"{self.for_chapter_part}"

class ChapterPartSummaryItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    for_chapter_part_outline = models.ForeignKey('ChapterPartSummary', on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField(blank=True)
    order_in_part = models.IntegerField(blank=True, default=0)
    
    def __str__(self):
        return f"{self.for_chapter_part_outline}-{self.order_in_part}"


# Background, Setting and Research

class Setting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    books = models.ManyToManyField('Book', blank=True)
    bg_events = models.ManyToManyField('BGEvent', blank=True)
    factions = models.ManyToManyField('Faction', blank=True)
    bg_research = models.OneToOneField('BGResearch', on_delete=models.SET_NULL, blank=True, null=True)
    general_setting = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name}"


class BGResearch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    bg_research = models.TextField(blank=True)
    deeper_bg_research_topic = models.ManyToManyField('DeeperBGResearchTopic', blank=True)

    def __str__(self):
        return f"{self.bg_research}"
    
class DeeperBGResearchTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    topic = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.topic

class BGEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    event = models.CharField(max_length=200)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_story_events = models.IntegerField(blank=True, null=True)
    order_in_narrative_telling = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.event

class Faction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    members = models.ManyToManyField('CharacterVersion', blank=True)
    
    def __str__(self):
        return self.name
    
class CharacterRelatedSettingTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    setting = models.ForeignKey('Setting', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
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

class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    book = models.ManyToManyField('Book')
    name = models.CharField(max_length=200)
    age_at_start = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=200, blank=True, null=True)
    sex = models.CharField(max_length=200, blank=True, null=True)
    sexuality = models.CharField(max_length=200, blank=True, null=True)
    origin = models.TextField(blank=True, null=True)
    representative_of = models.ManyToManyField('Theme', blank=True)
    permanent_characteristics = models.TextField(blank=True, null=True)
    versions = models.ManyToManyField('CharacterVersion', blank=True, null=True, related_name='+')
    elaboration = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class CharacterVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    for_character = models.ForeignKey('Character', blank=True, on_delete=models.SET_NULL, null=True)
    version_num = models.IntegerField()
    version_name = models.CharField(max_length=200, blank=True, null=True)
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
    elaboration = models.TextField(blank=True, null=True)
    lit_style_guides = models.ForeignKey('LitStyleGuide', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.for_character} v{self.version_num}"



class CharacterRelationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    relationship_from = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, related_name='has_relationship')
    relationship_to = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, related_name='character_relationship')
    age_started = models.IntegerField()
    relationship_descriptors = models.TextField()
    elaboration = models.TextField(blank=True, null=True)
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE, null=True, related_name='character_versions')

    def __str__(self):
        return f"{self.character_version}'s relationship with {self.relationship_to}"


class Appearance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    distinguishing_features = models.TextField()
    eyes = models.CharField(max_length=200)
    hair = models.CharField(max_length=200)
    face = models.CharField(max_length=200)
    build = models.CharField(max_length=200, blank=True, null=True)
    movement = models.CharField(max_length=200, blank=True, null=True)
    elaboration = models.TextField(blank=True, null=True)
    character_version = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, null=True, related_name='appearance_for_character_version')


class AppearanceModifiers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    clothing = models.TextField(blank=True, null=True)
    hair_head_options = models.TextField(blank=True, null=True)
    perfume = models.CharField(max_length=200, blank=True, null=True)
    makeup = models.CharField(max_length=200, blank=True, null=True)
    shaving = models.CharField(max_length=200, blank=True, null=True)
    hygiene = models.CharField(max_length=200, blank=True, null=True)
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.character_version}'s appearance"


class CharacterTrait(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Drive(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Fear(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Belief(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class InternalConflict(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    rel = models.CharField(max_length=200)
    character_version = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, blank=True, null=True, related_name='internal_conflict_character_version')

    def __str__(self):
        return self.name


class LitStyleGuide(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.SET_NULL, blank=True, null=True)
    perspective = models.ForeignKey('Perspective', on_delete=models.CASCADE)
    inspirations = models.ManyToManyField('LiteraryInspirationPerson', blank=True, null=True)
    traits = models.ManyToManyField('LiteraryTraits', related_name='litstyleguide_traits', blank=True)
    avoid = models.ManyToManyField('LiteraryTraits', related_name='litstyleguide_avoid', blank=True)
    style_guide = models.TextField(blank=True, null=True)
    compressed_sg = models.TextField(blank=True, null=True)
    writing_samples = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class LiteraryInspirationPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    person = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    sources = models.ManyToManyField('LiteraryInspirationSource', blank=True, null=True)
    
    def __str__(self):
        return self.person
    
class LiteraryInspirationSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    source = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.source

class StoryTeller(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    character = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE)
    style = models.ForeignKey('LitStyleGuide', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.character} style as a story teller"

class Theme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Perspective(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class LiteraryTraits(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Other

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    file_location = models.CharField(max_length=255)
    file_content = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.file_location


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    character_versions = models.ManyToManyField('CharacterVersion', blank=True, related_name='locations_in_character_version')
    
    def __str__(self):
        return self.name
