# Generated by Django 4.0.6 on 2023-04-17 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
    ]
