# Generated by Django 4.1.1 on 2022-11-14 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicstudios', '0011_frequentlyasked_alter_order_customer_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('before_mix', models.FileField(upload_to='')),
                ('after_mix', models.FileField(upload_to='')),
                ('song_name', models.CharField(max_length=100)),
                ('song_artist', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ['song_artist'],
            },
        ),
        migrations.AlterModelOptions(
            name='frequentlyasked',
            options={'verbose_name': 'Frequently Asked Question'},
        ),
    ]