# Generated by Django 4.1.1 on 2022-09-20 20:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Must be at least two characters.')])),
                ('release_date', models.DateField()),
                ('picture', models.ImageField(blank=True, upload_to='albums/')),
                ('content_type', models.CharField(blank=True, help_text='The MIMEType of the file', max_length=256)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Must be at least two characters.')])),
                ('release_date', models.DateField(blank=True)),
                ('length', models.CharField(max_length=200)),
                ('featured_artists', models.CharField(max_length=200)),
                ('picture', models.ImageField(blank=True, upload_to='albums/')),
                ('content_type', models.CharField(blank=True, help_text='The MIMEType of the file', max_length=256)),
                ('description', models.TextField(blank=True)),
                ('alb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.album')),
            ],
        ),
    ]