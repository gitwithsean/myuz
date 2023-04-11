# Generated by Django 4.2 on 2023-04-11 20:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("noveller", "0023_literaryinspiration_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LiteraryInspirationPerson",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        auto_created=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("person", models.CharField(max_length=200)),
                ("elaboration", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="LiteraryInspirationSource",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        auto_created=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("source", models.CharField(max_length=200)),
                ("elaboration", models.TextField(blank=True, null=True)),
                (
                    "person",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="noveller.literaryinspirationperson",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="LiteraryInspiration",
        ),
        migrations.AlterField(
            model_name="litstyleguide",
            name="inspirations",
            field=models.ManyToManyField(
                blank=True, null=True, to="noveller.literaryinspirationperson"
            ),
        ),
    ]
