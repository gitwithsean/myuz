# Generated by Django 4.2 on 2023-04-12 07:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("phusis", "0004_agentqualification_agenttrait_agent_elaboration_and_more"),
        (
            "noveller",
            "0041_alter_characterrelationship_agents_responsible_for_this_relationship",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="characterrelationship",
            name="agents_responsible_for_this_relationship",
            field=models.ManyToManyField(
                blank=True,
                related_name="relationships_agent_is_responsible_for",
                to="phusis.agent",
            ),
        ),
    ]