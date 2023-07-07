# Generated by Django 4.2 on 2023-05-11 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('noveller', '0003_rename_order_in_narrative_telling_scene_order_in_plot_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChapterPartSummaryItem',
            new_name='ChapterPartBreakdownItem',
        ),
        migrations.RenameField(
            model_name='character',
            old_name='versions',
            new_name='character_versions',
        ),
        migrations.RenameField(
            model_name='literarystyleguide',
            old_name='avoid',
            new_name='traits_to_avoid',
        ),
        migrations.RemoveField(
            model_name='backgroundevent',
            name='order_in_narrative_telling',
        ),
        migrations.RemoveField(
            model_name='chapterpart',
            name='chapter_part_summary',
        ),
        migrations.RemoveField(
            model_name='chapterpart',
            name='character_versions',
        ),
        migrations.RemoveField(
            model_name='chapterpart',
            name='factions',
        ),
        migrations.RemoveField(
            model_name='chapterpart',
            name='locations',
        ),
        migrations.RemoveField(
            model_name='chapterpartbreakdownitem',
            name='for_chapter_part_summary',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='pacing',
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='pacing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.storypacing'),
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='part_breakdown_items',
            field=models.ManyToManyField(blank=True, related_name='chapter_part_breakdown_items', to='noveller.chapterpartbreakdownitem'),
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='scene_for_chapter_part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chapter_parts_for_scene', to='noveller.scene'),
        ),
        migrations.AddField(
            model_name='chapterpartbreakdownitem',
            name='for_chapter_part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.chapterpart'),
        ),
        migrations.AddField(
            model_name='scene',
            name='factions',
            field=models.ManyToManyField(blank=True, to='noveller.faction'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='chapter_goals',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='chapterpart',
            name='part_goals',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterappearance',
            name='build',
            field=models.CharField(blank=True, default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='characterappearance',
            name='distinguishing_features',
            field=models.TextField(default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterappearance',
            name='eyes',
            field=models.CharField(default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='characterappearance',
            name='face',
            field=models.CharField(default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='characterappearance',
            name='hair',
            field=models.CharField(default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='characterappearance',
            name='movement',
            field=models.CharField(blank=True, default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='characterappearancemodifiers',
            name='clothing',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterappearancemodifiers',
            name='hair_head_options',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterappearancemodifiers',
            name='hygiene',
            field=models.CharField(blank=True, default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='characterappearancemodifiers',
            name='makeup',
            field=models.CharField(blank=True, default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='characterappearancemodifiers',
            name='perfume',
            field=models.CharField(blank=True, default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='characterappearancemodifiers',
            name='shaving',
            field=models.CharField(blank=True, default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='characterrelatedsettingtopic',
            name='attitudes',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterrelatedsettingtopic',
            name='food',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterrelatedsettingtopic',
            name='leisure',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterrelatedsettingtopic',
            name='rights',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterrelatedsettingtopic',
            name='social_life',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterrelatedsettingtopic',
            name='work',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterrelationship',
            name='relationship_descriptors',
            field=models.TextField(default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='characterversion',
            name='preferred_weapon',
            field=models.CharField(blank=True, default='not yet set', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='plot',
            name='plot_beginning',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='plot',
            name='plot_end',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.AlterField(
            model_name='plot',
            name='plot_middle',
            field=models.TextField(blank=True, default='not yet set', null=True),
        ),
        migrations.RemoveField(
            model_name='scene',
            name='for_plot',
        ),
        migrations.DeleteModel(
            name='ChapterPartSummary',
        ),
        migrations.AddField(
            model_name='scene',
            name='for_plot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plots_scenes', to='noveller.plot'),
        ),
    ]