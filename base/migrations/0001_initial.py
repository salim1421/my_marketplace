# Generated by Django 5.1.3 on 2024-12-01 14:00

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=299)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=299)),
                ('address', models.CharField(max_length=299)),
                ('website', models.CharField(max_length=299)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images')),
                ('name', models.CharField(max_length=299)),
                ('price', models.FloatField(default=0)),
                ('date_created', models.DateTimeField(default=datetime.datetime(2024, 12, 1, 14, 0, 34, 271123, tzinfo=datetime.timezone.utc))),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.cartitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('products', models.ManyToManyField(to='base.products')),
            ],
        ),
        migrations.AddField(
            model_name='cartitem',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.products'),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(max_length=299)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.category')),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.subcategory'),
        ),
    ]
