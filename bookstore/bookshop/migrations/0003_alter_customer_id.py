# Generated by Django 4.0.6 on 2023-04-18 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0002_remove_customer_address_remove_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]