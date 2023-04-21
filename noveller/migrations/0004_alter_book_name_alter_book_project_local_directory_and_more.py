# Generated by Django 4.2 on 2023-04-20 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phusis', '0005_remove_phusisscript_is_master_script'),
        ('noveller', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(default='book', max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='project_local_directory',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='script_for_project',
            field=models.OneToOneField(auto_created=True, blank=True, on_delete=django.db.models.deletion.PROTECT, to='phusis.phusisscript'),
        ),
    ]