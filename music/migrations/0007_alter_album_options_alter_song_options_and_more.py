# Generated by Django 4.1.1 on 2022-10-03 21:19

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_alter_album_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['-release_date']},
        ),
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['-release_date']},
        ),
        migrations.AlterModelManagers(
            name='song',
            managers=[
                ('only_singles', django.db.models.manager.Manager()),
            ],
        ),
    ]
