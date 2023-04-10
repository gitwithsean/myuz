from __future__ import annotations
from django.db import models

class Book(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    settings = models.ManyToManyField('Setting', blank=True)
    
    def __str__(self):
        return self.name

class StoryEvent(models.Model):
    uuid = models.UUIDField(primary_key=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_story_events = models.IntegerField(blank=True, null=True)
    order_in_narrative_telling = models.IntegerField(blank=True, null=True)
        
    def __str__(self):
        return f"Story Event: {self.description}"


#Chapters, Outlines, Summaries

class Chapter(models.Model):
    uuid = models.UUIDField(primary_key=True)
    books = models.ForeignKey('Book', on_delete=models.CASCADE)
    chapter_num = models.IntegerField()
    chapter_title = models.CharField(max_length=200, blank=True)
    chapter_file = models.OneToOneField('File', on_delete=models.SET_NULL, blank=True, null=True)
    chapter_outline = models.OneToOneField('ChapterOutline', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f"Chapter {self.chapter_num} {self.chapter_title}"


class ChapterPart(models.Model):
    uuid = models.UUIDField(primary_key=True)
    part_title = models.CharField(max_length=200, blank=True)
    part_num = models.IntegerField()
    teller = models.OneToOneField('StoryTeller', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.OneToOneField('Location', on_delete=models.SET_NULL, blank=True, null=True)
    chapter = models.ForeignKey('Chapter', on_delete=models.SET_NULL, blank=True, null=True)
    characters = models.ManyToManyField('CharacterVersion', blank=True)
    themes = models.ManyToManyField('Theme', blank=True)
    factions = models.ManyToManyField('Faction', blank=True)
    chapter_part_summary = models.ManyToManyField('ChapterPartOutline', blank=True)
    
    def __str__(self):
        return f"Part {self.part_num} of {self.chapter}"


class ChapterOutline(models.Model):
    uuid = models.UUIDField(primary_key=True)
    for_chapter = models.OneToOneField('Chapter', on_delete=models.SET_NULL, blank=True, null=True)
    summary = models.TextField(blank=True)
    story_event = models.ManyToManyField('StoryEvent', blank=True)
    chapter_part_outline = models.ManyToManyField('ChapterPartOutline', blank=True)
    
    def __str__(self):
        return f"Outline for {self.for_chapter}"


class ChapterPartOutline(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    for_chapter_part = models.OneToOneField('ChapterPart', on_delete=models.SET_NULL, blank=True, null=True)
    chapter_summary = models.TextField(blank=True)
    themes = models.ManyToManyField('Theme', blank=True)

    def __str__(self):
        return f"Outline for {self.for_chapter_part}"

class ChapterPartSummaryItem(models.Model):
    uuid = models.UUIDField(primary_key=True)
    for_chapter_part_outline = models.ForeignKey('ChapterPartOutline', on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.content}"


# Background, Setting and Research

class Setting(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    books = models.ManyToManyField('Book', blank=True)
    bg_events = models.ManyToManyField('BGEvent', blank=True)
    factions = models.ManyToManyField('Faction', blank=True)
    bg_research = models.OneToOneField('BGResearch', on_delete=models.SET_NULL, blank=True, null=True)
    general_setting = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name}"


class BGResearch(models.Model):
    uuid = models.UUIDField(primary_key=True)
    bg_research = models.TextField(blank=True)
    deeper_bg_research_topic = models.ManyToManyField('DeeperBGResearchTopic', blank=True)

    def __str__(self):
        return f"{self.bg_research}"
    
class DeeperBGResearchTopic(models.Model):
    uuid = models.UUIDField(primary_key=True)
    topic = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.notes

class BGEvent(models.Model):
    uuid = models.UUIDField(primary_key=True)
    event = models.CharField(max_length=200)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    order_in_story_events = models.IntegerField(blank=True, null=True)
    order_in_narrative_telling = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.event

class Faction(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    members = models.ManyToManyField('CharacterVersion', blank=True)
    
    def __str__(self):
        return self.name
    
class CharacterRelatedSettingTopic(models.Model):
    uuid = models.UUIDField(primary_key=True)
    setting = models.ForeignKey('Setting', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    character = models.ForeignKey('CharacterVersion', on_delete=models.SET_NULL, blank=True, null=True)
    rights = models.TextField()
    appearance_modifiers = models.ForeignKey('AppearanceModifiers', on_delete=models.SET_NULL, blank=True, null=True)
    attitudes = models.TextField()
    leisure = models.TextField()
    food = models.TextField()
    work = models.TextField()
    social_life = models.TextField()

    def __str__(self):
        return f"Setting as it relates to {self.character}"

class Character(models.Model):
    uuid = models.UUIDField(primary_key=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    age_at_start = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    sexuality = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    representative_of = models.ManyToManyField('Theme', blank=True)
    permanent_characteristics = models.TextField()
    elaboration = models.TextField(null=True, blank=True)
    relationship_for = models.OneToOneField('CharacterRelationship', blank=True, on_delete=models.SET_NULL, null=True, related_name='+')
    relationship_with = models.OneToOneField('CharacterRelationship', blank=True, on_delete=models.SET_NULL, null=True, related_name='+')
    lit_style_guides = models.ForeignKey('LitStyleGuide', blank=True, on_delete=models.SET_NULL, null=True, related_name='style_guide_for_character_perspective')

    def __str__(self):
        return self.name


class CharacterVersion(models.Model):
    uuid = models.UUIDField(primary_key=True)
    for_character = models.ForeignKey('Character', blank=True, on_delete=models.SET_NULL, null=True)
    version_num = models.IntegerField()
    version_name = models.CharField(max_length=200, blank=True, null=True)
    age_at_start = models.IntegerField()
    age_at_end = models.IntegerField()
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
    subter = models.CharField(max_length=200, blank=True, null=True)
    elaboration = models.TextField(blank=True, null=True)
    changes_from_previous_character_version = models.OneToOneField('ChangesFromPreviousCharacterVersion', null=True, blank=True, on_delete=models.SET_NULL)
    lit_style_guides = models.ForeignKey('LitStyleGuide', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.for_character} v{self.version_num}"

    
class ChangesFromPreviousCharacterVersion(CharacterVersion):
    previous_character_version = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, null=True, blank=True, related_name='previous_version')
    
    def __str__(self):
        return f"Changes to {self.previous_character_version}"


class CharacterRelationship(models.Model):
    uuid = models.UUIDField(primary_key=True)
    relationship_from = models.OneToOneField('Character', on_delete=models.CASCADE, related_name='has_relationship')
    relationship_to = models.OneToOneField('Character', on_delete=models.CASCADE, related_name='character_relationship')
    age_started = models.IntegerField()
    relationship_descriptors = models.TextField()
    elaboration = models.TextField(blank=True, null=True)
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE, null=True, related_name='character_versions')
    changes_from_previous_version = models.ForeignKey('ChangesFromPreviousCharacterVersion', on_delete=models.CASCADE, null=True, related_name='character_version_changes')

    def __str__(self):
        return f"{self.character_version}'s relationship with {self.relationship_to}"


class Appearance(models.Model):
    uuid = models.UUIDField(primary_key=True)
    distinguishing_features = models.TextField()
    eyes = models.CharField(max_length=200)
    hair = models.CharField(max_length=200)
    face = models.CharField(max_length=200)
    build = models.CharField(max_length=200, blank=True, null=True)
    movement = models.CharField(max_length=200, blank=True, null=True)
    elaboration = models.TextField(blank=True, null=True)
    changes_from_previous_character_version = models.OneToOneField('ChangesFromPreviousCharacterVersion', on_delete=models.CASCADE, null=True, related_name='version_appearane_change')
    character_version = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, null=True, related_name='appearance_for_character_version')


class AppearanceModifiers(models.Model):
    uuid = models.UUIDField(primary_key=True)
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
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Drive(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Fear(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Belief(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class InternalConflict(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    rel = models.CharField(max_length=200)
    character_version = models.OneToOneField('CharacterVersion', on_delete=models.CASCADE, blank=True, null=True, related_name='internal_conflict_character_version')
    changes_from_previous_character_version = models.OneToOneField('ChangesFromPreviousCharacterVersion', on_delete=models.CASCADE, blank=True, null=True, related_name='internal_conflict_changes_from_previous_character_version')

    def __str__(self):
        return self.name


class LitStyleGuide(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    character_version = models.ForeignKey('CharacterVersion', on_delete=models.SET_NULL, blank=True, null=True)
    perspective = models.ForeignKey('Perspective', on_delete=models.CASCADE)
    inspirations = models.TextField(blank=True, null=True)
    traits = models.ManyToManyField('LiteraryTraits', related_name='litstyleguide_traits', blank=True)
    avoid = models.ManyToManyField('LiteraryTraits', related_name='litstyleguide_avoid', blank=True)
    style_guide = models.TextField(blank=True, null=True)
    compressed_sg = models.TextField(blank=True, null=True)
    writing_samples = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class StoryTeller(models.Model):
    uuid = models.UUIDField(primary_key=True)
    character = models.ForeignKey('CharacterVersion', on_delete=models.CASCADE)
    style = models.ForeignKey('LitStyleGuide', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.character} style as a story teller"

class Theme(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Perspective(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    lit_style_guides = models.ForeignKey('LitStyleGuide', on_delete=models.CASCADE, related_name='perspectives')
    
    def __str__(self):
        return self.name


class LiteraryTraits(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    lit_style_guide_traits = models.ManyToManyField('LitStyleGuide', related_name='litstyleguide_traits', blank=True)
    lit_style_guide_avoid = models.ManyToManyField('LitStyleGuide', related_name='litstyleguide_avoid', blank=True)
    
    def __str__(self):
        return self.name

# Other

class File(models.Model):
    uuid = models.UUIDField(primary_key=True)
    file_location = models.CharField(max_length=255)
    file_content = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.file_location


class Location(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    elaboration = models.TextField(blank=True, null=True)
    character_versions = models.ManyToManyField('CharacterVersion', blank=True, related_name='locations_in_character_version')
    
    def __str__(self):
        return self.name

