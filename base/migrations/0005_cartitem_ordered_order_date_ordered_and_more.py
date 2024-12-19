# Generated by Django 5.1.3 on 2024-12-13 21:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_order_ordered_remove_order_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RemoveField(
            model_name='order',
            name='cart_item',
        ),
        migrations.AddField(
            model_name='order',
            name='cart_item',
            field=models.ManyToManyField(to='base.cartitem'),
        ),
    ]
