# Generated by Django 4.2 on 2023-04-12 04:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("noveller", "0035_alter_chapterpartsummaryitem_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subplotevent",
            options={"ordering": ["order_in_story_events"]},
        ),
        migrations.RemoveField(
            model_name="plotevent",
            name="book",
        ),
        migrations.RemoveField(
            model_name="subplotevent",
            name="sub_plot_of",
        ),
        migrations.CreateModel(
            name="Plot",
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
                ("title", models.CharField(max_length=200)),
                ("elaboration", models.TextField(blank=True, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books_plots",
                        to="noveller.book",
                    ),
                ),
                (
                    "events_of_plot",
                    models.ManyToManyField(blank=True, to="noveller.plotevent"),
                ),
            ],
            options={
                "ordering": ["title"],
            },
        ),
        migrations.AddField(
            model_name="plotevent",
            name="subplot_of",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plots_events",
                to="noveller.plot",
            ),
        ),
        migrations.CreateModel(
            name="SubPlot",
            fields=[
                (
                    "plot_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="noveller.plot",
                    ),
                ),
                (
                    "events_of_subplot",
                    models.ManyToManyField(
                        blank=True,
                        related_name="subplots_events",
                        to="noveller.subplotevent",
                    ),
                ),
                (
                    "sub_plot_of",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plots_subplot",
                        to="noveller.plot",
                    ),
                ),
            ],
            options={
                "ordering": ["sub_plot_of__title", "title"],
            },
            bases=("noveller.plot",),
        ),
        migrations.AddField(
            model_name="subplotevent",
            name="subplot",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subplots_events",
                to="noveller.subplot",
            ),
        ),
    ]
