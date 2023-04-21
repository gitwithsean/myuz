# Generated by Django 4.2 on 2023-04-21 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noveller', '0005_remove_book_script_for_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='project_local_directory',
            new_name='project_workspace',
        ),
        migrations.RemoveField(
            model_name='book',
            name='project_files_added_paths',
        ),
        migrations.RemoveField(
            model_name='book',
            name='project_files_produced_paths',
        ),
        migrations.RemoveField(
            model_name='book',
            name='project_user_inputs',
        ),
        migrations.AddField(
            model_name='book',
            name='project_user_input',
            field=models.TextField(blank=True, default=''),
        ),
    ]
