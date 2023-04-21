# Generated by Django 4.2 on 2023-04-21 02:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('phusis', '0006_remove_characteragent_script_for_agent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agentbookrelationship',
            name='id',
        ),
        migrations.AlterField(
            model_name='agentbookrelationship',
            name='object_id',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]