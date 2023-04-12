# Generated by Django 4.2 on 2023-04-11 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("noveller", "0030_alter_character_origin"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="chapters",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="books_chapters",
                to="noveller.chapter",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="characters",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="characters_book_characters",
                to="noveller.character",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="events",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="books_events",
                to="noveller.storyevent",
            ),
        ),
        migrations.AlterField(
            model_name="chapter",
            name="books",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="book_characters",
                to="noveller.book",
            ),
        ),
        migrations.RemoveField(
            model_name="character",
            name="book",
        ),
        migrations.AlterField(
            model_name="storyevent",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="books_story_events",
                to="noveller.book",
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="book",
            field=models.ManyToManyField(to="noveller.book"),
        ),
    ]