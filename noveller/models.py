from __future__ import annotations
from typing import List, Optional, Union
from django.db import models

class Novel(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    story_outline = models.OneToManyField('StoryEvent', on_delete=models.CASCADE, blank=True)
    chapters = models.OneToManyField('Chapter', on_delete=models.CASCADE, blank=True)
    setting = models.OneToOne('Setting', on_delete=models.CASCADE, blank=True)
    characters = models.OneToManyField('Character', on_delete=models.CASCADE,  blank=True)
    def __str__(self):
        return self.name

class StoryEvent(models.Model):
    uuid = models.UUIDField(primary_key=True)
    locations = models.OneToManyField('Location', on_delete=models.CASCADE, blank=True)
    characters = models.OneToManyField('Character', on_delete=models.CASCADE,  blank=True)
    description = models.CharField(max_length=200)
    when = models.OneToOneField('YearItem', on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return f"Story Event: {self.description}"

#Chapters, Outlines, Summaries

class Chapter(models.Model):
    uuid = models.UUIDField(primary_key=True)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    chapter_num = models.IntegerField
    chapter_title = models.CharField(blank=True, max_length=100)
    chapter_file = models.OneToOneField('File', on_delete=models.CASCADE, blank=True)
    chapter_parts = models.OneToManyField('ChapterPart', on_delete=models.CASCADE,  blank=True)
    chapter_outline = models.OneToOneField('ChapterOutline', on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return f"Chapter - {self.chapter_num} {self.chapter_title}"

class ChapterPart(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    teller: StoryTeller
    location: Location
    characters: List[CharacterVersion]
    themes: List[Theme]
    factions: List[Faction]
    chapter_part_summary: List[ChapterPartOutline]

class ChapterOutline(models.Model):
    uuid = models.UUIDField(primary_key=True)
    story_event: List[StoryEvent]
    for_chapter: Chapter
    summary: str
    chapter_part_outline: List[ChapterPartOutline]

class ChapterPartOutline(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    for_chapter_part: ChapterPart
    themes: List[Theme]
    chapter_summary: Union[str, List[ChapterPartSummaryItem]]
    
class ChapterPartSummaryItem(models.Model):
    uuid = models.UUIDField(primary_key=True)
    content: str


# Background, Setting and Research

class Setting(models.Model):
    uuid = models.UUIDField(primary_key=True)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    general_setting: List[str]
    bg_research: BGResearch
    character_related_setting_info: List[CharacterRelatedSettingTopic]
    bg_events: List[BGEvent]
    factions: List[Faction]

class BGResearch(models.Model):
    uuid = models.UUIDField(primary_key=True)
    bg_research: Optional[List[str]] = None
    deeper_bg_research_topic: Optional[List[DeeperBGResearchTopic]] = None
     
class DeeperBGResearchTopic(models.Model):
    uuid = models.UUIDField(primary_key=True)
    topic: str
    notes: List[str]
    
class BGEvent(models.Model):
    uuid = models.UUIDField(primary_key=True)
    event: str
    when: YearItem

class Faction(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    description: Optional[str] = None
    members: Optional[List[CharacterVersion]] = None

class CharacterRelatedSettingTopic(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    character: CharacterVersion
    rights: List[str]
    appearance_modifiers: AppearanceModifiers
    attitudes: List[str]
    leisure: List[str]
    food: List[str]
    work: List[str]
    social_life: List[str]


#Characters, Traits, Relationships

class Character(models.Model):
    uuid = models.UUIDField(primary_key=True)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    name: str
    age_at_start: Optional[models.IntegerField]=None
    gender: str
    sex: str
    sexuality: str
    origin: str
    representative_of: List[Theme]
    permanent_characteristics: List[str]
    versions: List[CharacterVersion]
    elaboration: Optional[str]=None

class CharacterVersion(models.Model):
    uuid = models.UUIDField(primary_key=True)
    version = models.IntegerField
    version_name: str
    age_at_start = models.IntegerField
    age_at_end = models.IntegerField
    locations: List[Location]
    preferred_weapon: Optional[str] = None
    appearance: Optional[Appearance] = None
    setting_based_appearance_modifier_options: Optional[AppearanceModifiers] = None
    strengths: Optional[List[CharacterTrait]] = None
    weaknesses: Optional[List[CharacterTrait]] = None
    other_aspects: Optional[List[CharacterTrait]] = None
    often_perceived_as: Optional[List[CharacterTrait]] = None
    drives: Optional[List[Drive]] = None
    fears: Optional[List[Fear]] = None
    beliefs: Optional[Belief] = None
    models.IntegerFieldernal_conflicts: Optional[models.IntegerFieldernalConflict] = None
    subter: Optional[str] = None
    relationships: List[CharacterRelationship]
    changes_from_previous_version: Optional[ChangesFromPreviousCharacterVersion] = None
    elaboration: Optional[str]=None
    
class ChangesFromPreviousCharacterVersion(models.Model):
    uuid = models.UUIDField(primary_key=True)
    version = models.IntegerField
    version_name: str
    age_at_start = models.IntegerField
    age_at_end = models.IntegerField
    locations: Optional[List[Location]]
    preferred_weapon: Optional[str] = None
    appearance: Optional[Appearance] = None
    setting_based_appearance_modifier_options: Optional[AppearanceModifiers] = None
    strengths: Optional[List[CharacterTrait]] = None
    weaknesses: Optional[List[CharacterTrait]] = None
    other_aspects: Optional[List[CharacterTrait]] = None
    often_perceived_as: Optional[List[CharacterTrait]] = None
    drives: Optional[List[Drive]] = None
    fears: Optional[List[Fear]] = None
    beliefs: Optional[Belief] = None
    models.IntegerFieldernal_conflicts: Optional[List] = None
    subter: Optional[str] = None
    relationships: Optional[List[CharacterRelationship]]
    elaboration: Optional[str]=None

class CharacterRelationship(models.Model):
    relationship_for: Character
    relationship_with: Character
    age_it_started = models.IntegerField
    rel: List[str]
    elaboration: Optional[str]=None

class Appearance(models.Model):
    uuid = models.UUIDField(primary_key=True)
    distinguishing_features: List[str]
    eyes: str
    hair: str
    face: str
    build: str
    movement: str
    elaboration: Optional[str]=None

class AppearanceModifiers(models.Model):
    uuid = models.UUIDField(primary_key=True)
    clothing: List[str]
    hair_head_options: List[str]
    perfume: str
    makeup: str
    shaving: str
    hygiene: str

class CharacterTrait:
    uuid = models.UUIDField(primary_key=True)
    name: str
    elaboration: Optional[str]=None
    
class Drive:
    uuid = models.UUIDField(primary_key=True)
    name: str
    elaboration: Optional[str]=None
       
class Fear:
    uuid = models.UUIDField(primary_key=True)
    name: str
    elaboration: Optional[str]=None
           
class Belief:
    uuid = models.UUIDField(primary_key=True)
    name: str
    elaboration: Optional[str]=None

class Location(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    elaboration: Optional[str]=None
    
class models.IntegerFieldernalConflict(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    rel: str


#Literary Styles, Themes, Perspectives

class LitStyleGuide(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    character: Character
    character_version: Optional[CharacterVersion] = None
    perspective: Perspective
    inspirations: Optional[List[str]] = None
    traits: Optional[List[LiteraryTraits]] = None
    avoid: Optional[List[LiteraryTraits]] = None
    style_guide: List[str] = None
    compressed_sg: Optional[List[str]] = None
    writing_samples: Optional[List[str]] = None

class StoryTeller(models.Model):
    uuid = models.UUIDField(primary_key=True)
    character: CharacterVersion
    style: LitStyleGuide
    description: Optional[str] = None    
    
class Theme(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    elaboration: str

#First person etc.
class Perspective(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    elaboration: str

class LiteraryTraits(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name: str
    elaboration: str


#Other

class YearItem(models.Model):
    from_: float = Field(..., alias='from')
    to: float

class File(models.Model):
    uuid = models.UUIDField(primary_key=True)
    file_locations: str
    file_content: Optional[str] = None

class Model(models.Model):
    novel: Novel
    story_events: List[StoryEvent]
    chapters: List[Chapter]
    setting: Setting
    characters: List[Character]
    style_guides: List[LitStyleGuide]
