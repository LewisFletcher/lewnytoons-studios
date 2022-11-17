# Generated by Django 4.1.1 on 2022-09-20 23:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='blog_photo1_ex',
            field=models.TextField(blank=True, help_text='Information displayed below the picture. Optional.'),
        ),
        migrations.AddField(
            model_name='post',
            name='blog_photo2_ex',
            field=models.TextField(blank=True, help_text='Information displayed below the picture. Optional.'),
        ),
        migrations.AlterField(
            model_name='post',
            name='blog_photo1',
            field=models.ImageField(blank=True, help_text='Displayed in the preview and the top of the blog post.', upload_to='blog_photos/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='blog_photo2',
            field=models.ImageField(blank=True, help_text='Displayed before the final textbox, after the second textbox.', upload_to='blog_photos/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='blog_textbox1',
            field=models.TextField(help_text='Displayed in the preview.'),
        ),
        migrations.AlterField(
            model_name='post',
            name='blog_textbox2',
            field=models.TextField(help_text='Displayed after the first textbox on the detail page.'),
        ),
        migrations.AlterField(
            model_name='post',
            name='blog_textbox3',
            field=models.TextField(help_text='Displayed after the second image on the detail page.'),
        ),
        migrations.AlterField(
            model_name='post',
            name='summary',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(20, 'Displayed in the preview and top of the article.')]),
        ),
    ]