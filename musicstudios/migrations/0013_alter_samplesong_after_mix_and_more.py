# Generated by Django 4.1.1 on 2022-11-14 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicstudios', '0012_samplesong_alter_frequentlyasked_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samplesong',
            name='after_mix',
            field=models.FileField(upload_to='studio_samples/'),
        ),
        migrations.AlterField(
            model_name='samplesong',
            name='before_mix',
            field=models.FileField(upload_to='studio_samples/'),
        ),
    ]