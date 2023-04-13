# Generated by Django 4.2 on 2023-04-13 08:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("noveller", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bgevent",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="bgresearch",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="deeperbgresearchtopic",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="file",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="literaryinspirationperson",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="literaryinspirationsource",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="novellormodellor",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="plot",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="plotevent",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="subplot",
            options={"ordering": ["sub_plot_of__name", "name"]},
        ),
        migrations.RemoveField(
            model_name="deeperbgresearchtopic",
            name="topic",
        ),
        migrations.RemoveField(
            model_name="internalconflict",
            name="character_version",
        ),
        migrations.RemoveField(
            model_name="internalconflict",
            name="rel",
        ),
        migrations.RemoveField(
            model_name="novellormodellor",
            name="user",
        ),
        migrations.RemoveField(
            model_name="plot",
            name="title",
        ),
        migrations.RemoveField(
            model_name="storyteller",
            name="description",
        ),
        migrations.AddField(
            model_name="appearancemodifiers",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bgevent",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bgresearch",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="chapter",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="chapterpart",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="chapterpartsummary",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="chapterpartsummaryitem",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="characterrelatedsettingtopic",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="deeperbgresearchtopic",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="faction",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="file",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="internalconflict",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="litstyleguide",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="novellormodellor",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="plotevent",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="setting",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="storyteller",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="chapterpartsummary",
            name="name",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="characterrelatedsettingtopic",
            name="name",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="pacing",
            name="elaboration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="pacing",
            name="name",
            field=models.CharField(max_length=200),
        ),
    ]
