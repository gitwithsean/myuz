# Generated by Django 4.2 on 2023-05-16 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phusis', '0010_rename_object_id_agentassignment_agent_object_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='concreteabstractagent',
            old_name='awake',
            new_name='is_awake',
        ),
        migrations.RenameField(
            model_name='dynamicagent',
            old_name='awake',
            new_name='is_awake',
        ),
        migrations.RenameField(
            model_name='orchestrationagent',
            old_name='awake',
            new_name='is_awake',
        ),
        migrations.RenameField(
            model_name='useragentsingleton',
            old_name='awake',
            new_name='is_awake',
        ),
        migrations.RemoveField(
            model_name='concreteabstractagent',
            name='steps_taken',
        ),
        migrations.RemoveField(
            model_name='dynamicagent',
            name='steps_taken',
        ),
        migrations.RemoveField(
            model_name='orchestrationagent',
            name='steps_taken',
        ),
        migrations.RemoveField(
            model_name='useragentsingleton',
            name='steps_taken',
        ),
        migrations.AddField(
            model_name='concreteabstractagent',
            name='model_override',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dynamicagent',
            name='model_override',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orchestrationagent',
            name='model_override',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='useragentsingleton',
            name='model_override',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
