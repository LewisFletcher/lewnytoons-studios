# Generated by Django 4.1.1 on 2022-11-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicstudios', '0010_alter_customer_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrequentlyAsked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_paid',
            field=models.FloatField(default=0),
        ),
    ]
