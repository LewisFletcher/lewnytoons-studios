# Generated by Django 4.1.1 on 2022-10-12 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_blog_photo1_ex_post_blog_photo2_ex_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]
