# Generated by Django 5.1.3 on 2024-12-13 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_products_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]