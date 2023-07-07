# Generated by Django 4.2 on 2023-05-11 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('phusis', '0004_phusisprojectgoal_on_hold_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phusisprojectgoalstep',
            name='related_project_attributes',
        ),
        migrations.AddField(
            model_name='phusisprojectgoalstep',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='phusisprojectgoalstep',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]