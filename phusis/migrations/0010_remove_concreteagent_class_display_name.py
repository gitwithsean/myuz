# Generated by Django 4.2 on 2023-04-17 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phusis', '0009_alter_concreteagent_class_display_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concreteagent',
            name='class_display_name',
        ),
    ]
