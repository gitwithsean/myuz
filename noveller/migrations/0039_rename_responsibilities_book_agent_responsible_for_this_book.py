# Generated by Django 4.2 on 2023-04-12 06:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("noveller", "0038_alter_book_responsibilities"),
    ]

    operations = [
        migrations.RenameField(
            model_name="book",
            old_name="responsibilities",
            new_name="agent_responsible_for_this_book",
        ),
    ]
