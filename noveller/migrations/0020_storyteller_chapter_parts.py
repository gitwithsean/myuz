# Generated by Django 4.2 on 2023-04-11 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("noveller", "0019_remove_literarytraits_lit_style_guide_avoid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="storyteller",
            name="chapter_parts",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="noveller.chapterpart",
            ),
        ),
    ]
