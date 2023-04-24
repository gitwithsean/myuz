# Generated by Django 4.2 on 2023-04-24 17:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('noveller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appearance',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('distinguishing_features', models.TextField()),
                ('eyes', models.CharField(max_length=200)),
                ('hair', models.CharField(max_length=200)),
                ('face', models.CharField(max_length=200)),
                ('build', models.CharField(blank=True, max_length=200, null=True)),
                ('movement', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['character_version__for_character__name', 'character_version__version_num'],
            },
        ),
        migrations.CreateModel(
            name='AppearanceModifiers',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('clothing', models.TextField(blank=True, null=True)),
                ('hair_head_options', models.TextField(blank=True, null=True)),
                ('perfume', models.CharField(blank=True, max_length=200, null=True)),
                ('makeup', models.CharField(blank=True, max_length=200, null=True)),
                ('shaving', models.CharField(blank=True, max_length=200, null=True)),
                ('hygiene', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['character_version__for_character__name', 'character_version__version_num'],
            },
        ),
        migrations.CreateModel(
            name='BackgroundEvent',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('date_from', models.DateField(blank=True, null=True)),
                ('date_to', models.DateField(blank=True, null=True)),
                ('order_in_story_events', models.IntegerField(blank=True, null=True)),
                ('order_in_narrative_telling', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BackgroundResearch',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('research', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Belief',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', max_length=200, unique=True)),
                ('project_type', models.CharField(default='Book', max_length=200)),
                ('project_user_input', models.TextField(blank=True, default='')),
                ('project_workspace', models.CharField(default='', max_length=200)),
                ('orc_agent_set_objectives', models.TextField(blank=True, default='')),
                ('project_embedding', models.TextField(blank=True)),
                ('from_app', models.CharField(default='noveller', max_length=200)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('expose_rest', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('chapter_num', models.IntegerField()),
                ('chapter_goals', models.TextField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_characters', to='noveller.book')),
            ],
            options={
                'ordering': ['chapter_num'],
            },
        ),
        migrations.CreateModel(
            name='ChapterPart',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('part_num', models.IntegerField()),
                ('part_goals', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['for_chapter__chapter_num', 'part_num'],
            },
        ),
        migrations.CreateModel(
            name='ChapterPartSummary',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('chapter_part_summary', models.TextField(blank=True)),
                ('for_chapter_part', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.chapterpart')),
            ],
            options={
                'ordering': ['for_chapter_part__for_chapter__chapter_num', 'for_chapter_part__part_num'],
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('age_at_start', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=200, null=True)),
                ('sex', models.CharField(blank=True, max_length=200, null=True)),
                ('sexuality', models.CharField(blank=True, max_length=200, null=True)),
                ('origin', models.TextField(blank=True, null=True)),
                ('permanent_characteristics', models.TextField(blank=True, null=True)),
                ('character_arc', models.TextField(blank=True, null=True)),
                ('books', models.ManyToManyField(to='noveller.book')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CharacterRelationship',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('age_started', models.IntegerField()),
                ('relationship_descriptors', models.TextField()),
            ],
            options={
                'ordering': ['relationship_from__for_character__name', 'relationship_to__for_character__name'],
            },
        ),
        migrations.CreateModel(
            name='CharacterTrait',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CharacterVersion',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('version_num', models.IntegerField()),
                ('age_at_start', models.IntegerField(blank=True, null=True)),
                ('age_at_end', models.IntegerField(blank=True, null=True)),
                ('preferred_weapon', models.CharField(blank=True, max_length=200, null=True)),
                ('subter', models.CharField(blank=True, max_length=200, null=True)),
                ('appearance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.appearance')),
                ('beliefs', models.ManyToManyField(blank=True, to='noveller.belief')),
            ],
            options={
                'ordering': ['for_character__name'],
            },
        ),
        migrations.CreateModel(
            name='DeeperBackgroundResearchTopic',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Faction',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('members', models.ManyToManyField(blank=True, to='noveller.characterversion')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fear',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('file_location', models.CharField(max_length=255)),
                ('file_content', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InternalConflict',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiteraryImagery',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiteraryInspirationPerson',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiteraryInspirationSource',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiteraryMood',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiterarySymbolism',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiteraryTheme',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiteraryTone',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiteraryTrait',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LitStyleGuide',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('style_guide', models.TextField(blank=True, null=True)),
                ('compressed_sg', models.TextField(blank=True, null=True)),
                ('writing_samples', models.TextField(blank=True, null=True)),
                ('avoid', models.ManyToManyField(blank=True, related_name='litstyleguide_avoid', to='noveller.literarytrait')),
                ('imagery', models.ManyToManyField(blank=True, to='noveller.literaryimagery')),
                ('inspirations', models.ManyToManyField(blank=True, to='noveller.literaryinspirationperson')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NarrativePerspective',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NovellerModellor',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pacing',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_plots', to='noveller.book')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlotEvent',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('date_from', models.DateField(blank=True, null=True)),
                ('date_to', models.DateField(blank=True, null=True)),
                ('order_in_story_events', models.IntegerField(blank=True, null=True)),
                ('order_in_narrative_telling', models.IntegerField(blank=True, null=True)),
                ('is_climax_of_plot', models.BooleanField(blank=True, null=True)),
                ('for_plot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plots_events', to='noveller.plot')),
                ('foreshadowing', models.ManyToManyField(blank=True, related_name='SubPlotEvent', to='noveller.plotevent')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TargetAudience',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubPlot',
            fields=[
                ('plot_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='noveller.plot')),
            ],
            options={
                'ordering': ['sub_plot_of__name', 'name'],
            },
            bases=('noveller.plot',),
        ),
        migrations.CreateModel(
            name='SubPlotEvent',
            fields=[
                ('plotevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='noveller.plotevent')),
            ],
            options={
                'ordering': ['order_in_story_events'],
            },
            bases=('noveller.plotevent',),
        ),
        migrations.CreateModel(
            name='StoryTeller',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('character_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noveller.characterversion')),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noveller.litstyleguide')),
            ],
            options={
                'ordering': ['character_version__for_character__name'],
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('general_setting', models.TextField(blank=True)),
                ('background_events', models.ManyToManyField(blank=True, to='noveller.backgroundevent')),
                ('background_research', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.backgroundresearch')),
                ('books', models.ManyToManyField(blank=True, to='noveller.book')),
                ('factions', models.ManyToManyField(blank=True, to='noveller.faction')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='plot',
            name='events_of_plot',
            field=models.ManyToManyField(blank=True, to='noveller.plotevent'),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('character_versions', models.ManyToManyField(blank=True, related_name='locations_in_character_version', to='noveller.characterversion')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='litstyleguide',
            name='perspective',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noveller.narrativeperspective'),
        ),
        migrations.AddField(
            model_name='litstyleguide',
            name='symbolism',
            field=models.ManyToManyField(blank=True, to='noveller.literarysymbolism'),
        ),
        migrations.AddField(
            model_name='litstyleguide',
            name='tone',
            field=models.ManyToManyField(blank=True, to='noveller.literarytone'),
        ),
        migrations.AddField(
            model_name='litstyleguide',
            name='traits',
            field=models.ManyToManyField(blank=True, related_name='litstyleguide_traits', to='noveller.literarytrait'),
        ),
        migrations.AddField(
            model_name='literaryinspirationperson',
            name='sources',
            field=models.ManyToManyField(blank=True, to='noveller.literaryinspirationsource'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='drives',
            field=models.ManyToManyField(blank=True, to='noveller.drive'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='fears',
            field=models.ManyToManyField(blank=True, to='noveller.fear'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='for_character',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.character'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='internal_conflicts',
            field=models.ManyToManyField(blank=True, to='noveller.internalconflict'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='lit_style_guides',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.litstyleguide'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='locations',
            field=models.ManyToManyField(blank=True, to='noveller.location'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='often_perceived_as',
            field=models.ManyToManyField(blank=True, related_name='often_perceived_as', to='noveller.charactertrait'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='other_aspects',
            field=models.ManyToManyField(blank=True, related_name='other_aspects', to='noveller.charactertrait'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='relationship_for',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='noveller.characterrelationship'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='relationship_with',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='noveller.characterrelationship'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='setting_based_appearance_modifier_options',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.appearancemodifiers'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='strengths',
            field=models.ManyToManyField(blank=True, related_name='strengths', to='noveller.charactertrait'),
        ),
        migrations.AddField(
            model_name='characterversion',
            name='weaknesses',
            field=models.ManyToManyField(blank=True, related_name='weaknesses', to='noveller.charactertrait'),
        ),
        migrations.AddField(
            model_name='characterrelationship',
            name='relationship_from',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='has_relationship', to='noveller.characterversion'),
        ),
        migrations.AddField(
            model_name='characterrelationship',
            name='relationship_to',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='character_relationship', to='noveller.characterversion'),
        ),
        migrations.CreateModel(
            name='CharacterRelatedSettingTopic',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('rights', models.TextField(blank=True, null=True)),
                ('attitudes', models.TextField(blank=True, null=True)),
                ('leisure', models.TextField(blank=True, null=True)),
                ('food', models.TextField(blank=True, null=True)),
                ('work', models.TextField(blank=True, null=True)),
                ('social_life', models.TextField(blank=True, null=True)),
                ('appearance_modifiers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.appearancemodifiers')),
                ('setting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.setting')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='character',
            name='representative_of',
            field=models.ManyToManyField(blank=True, to='noveller.literarytheme'),
        ),
        migrations.AddField(
            model_name='character',
            name='versions',
            field=models.ManyToManyField(blank=True, related_name='+', to='noveller.characterversion'),
        ),
        migrations.CreateModel(
            name='ChapterPartSummaryItem',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('elaboration', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True)),
                ('order_in_part', models.IntegerField(blank=True, default=0)),
                ('for_chapter_part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.chapterpartsummary')),
            ],
            options={
                'ordering': ['for_chapter_part__for_chapter_part__for_chapter__book', 'for_chapter_part__for_chapter_part__for_chapter__chapter_num', 'for_chapter_part__for_chapter_part__part_num', 'order_in_part'],
            },
        ),
        migrations.AddField(
            model_name='chapterpartsummary',
            name='pacing',
            field=models.ManyToManyField(blank=True, to='noveller.pacing'),
        ),
        migrations.AddField(
            model_name='chapterpartsummary',
            name='part_summary_items',
            field=models.ManyToManyField(related_name='chapter_part_summary_items', to='noveller.chapterpartsummaryitem'),
        ),
        migrations.AddField(
            model_name='chapterpartsummary',
            name='themes',
            field=models.ManyToManyField(blank=True, to='noveller.literarytheme'),
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='chapter_part_summary',
            field=models.ManyToManyField(blank=True, to='noveller.chapterpartsummary'),
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='characters',
            field=models.ManyToManyField(blank=True, to='noveller.characterversion'),
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='factions',
            field=models.ManyToManyField(blank=True, to='noveller.faction'),
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='for_chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chapter_parts', to='noveller.chapter'),
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='locations',
            field=models.ManyToManyField(blank=True, to='noveller.location'),
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='teller',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.storyteller'),
        ),
        migrations.AddField(
            model_name='chapterpart',
            name='themes',
            field=models.ManyToManyField(blank=True, to='noveller.literarytheme'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='chapter_draft_file',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noveller.file'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='parts_for_chapter',
            field=models.ManyToManyField(blank=True, related_name='chapters', to='noveller.chapterpart'),
        ),
    ]
