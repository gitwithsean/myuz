# Generated by Django 4.2 on 2023-04-11 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("noveller", "0003_alter_storyevent_book"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="storyevent",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="books",
                to="noveller.storyevent",
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="settings",
            field=models.ManyToManyField(
                blank=True, related_name="book_settings", to="noveller.setting"
            ),
        ),
    ]