# Generated by Django 4.1.1 on 2022-10-12 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stripe_product_id', models.CharField(max_length=100)),
                ('product_description', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_price_id', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('price_description', models.CharField(max_length=300, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicstudios.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_requests', models.CharField(max_length=1000, null=True)),
                ('reference_track', models.CharField(max_length=200, null=True)),
                ('music_file', models.FileField(upload_to='studio_orders/')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicstudios.customer')),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicstudios.price')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicstudios.product')),
            ],
        ),
    ]
