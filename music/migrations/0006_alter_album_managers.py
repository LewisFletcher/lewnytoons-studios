# Generated by Django 4.1.1 on 2022-10-03 21:08

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_song_audio_file'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='album',
            managers=[
                ('only_albums', django.db.models.manager.Manager()),
            ],
        ),
    ]
