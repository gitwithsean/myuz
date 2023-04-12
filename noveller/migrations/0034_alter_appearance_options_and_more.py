# Generated by Django 4.2 on 2023-04-12 04:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("noveller", "0033_alter_plotevent_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="appearance",
            options={
                "ordering": [
                    "character_version__for_character__name",
                    "character_version__version_num",
                ]
            },
        ),
        migrations.AlterModelOptions(
            name="appearancemodifiers",
            options={
                "ordering": [
                    "character_version__for_character__name",
                    "character_version__version_num",
                ]
            },
        ),
        migrations.AlterModelOptions(
            name="belief",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="bgevent",
            options={"ordering": ["date_from"]},
        ),
        migrations.AlterModelOptions(
            name="bgresearch",
            options={"ordering": ["bg_research"]},
        ),
        migrations.AlterModelOptions(
            name="book",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="chapter",
            options={"ordering": ["chapter_num"]},
        ),
        migrations.AlterModelOptions(
            name="chapterpart",
            options={"ordering": ["chapter__chapter_num", "part_num"]},
        ),
        migrations.AlterModelOptions(
            name="chapterpartsummary",
            options={
                "ordering": [
                    "for_chapter_part__chapter__chapter_num",
                    "for_chapter_part__part_num",
                ]
            },
        ),
        migrations.AlterModelOptions(
            name="chapterpartsummaryitem",
            options={
                "ordering": [
                    "for_chapter_part_outline__for_chapter_part__chapter__book",
                    "for_chapter_part_outline__for_chapter_part__chapter__chapter_num",
                    "for_chapter_part_outline__for_chapter_part__part_num",
                    "order_in_part",
                ]
            },
        ),
        migrations.AlterModelOptions(
            name="character",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="characterrelatedsettingtopic",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="characterrelationship",
            options={
                "ordering": [
                    "relationship_from__for_character__name",
                    "relationship_to__for_character__name",
                ]
            },
        ),
        migrations.AlterModelOptions(
            name="charactertrait",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="characterversion",
            options={"ordering": ["for_character__name", "version_num"]},
        ),
        migrations.AlterModelOptions(
            name="deeperbgresearchtopic",
            options={"ordering": ["topic"]},
        ),
        migrations.AlterModelOptions(
            name="drive",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="faction",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="fear",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="genre",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="internalconflict",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="literaryimagery",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="literaryinspirationperson",
            options={"ordering": ["person"]},
        ),
        migrations.AlterModelOptions(
            name="literaryinspirationsource",
            options={"ordering": ["source"]},
        ),
        migrations.AlterModelOptions(
            name="literarymood",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="literarysymbolism",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="literarytone",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="literarytraits",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="litstyleguide",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="location",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="pacing",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="perspective",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="setting",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="storyteller",
            options={"ordering": ["character__for_character__name"]},
        ),
        migrations.AlterModelOptions(
            name="targetaudience",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="theme",
            options={"ordering": ["name"]},
        ),
        migrations.RenameField(
            model_name="chapter",
            old_name="books",
            new_name="book",
        ),
    ]