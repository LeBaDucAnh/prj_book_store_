# Generated by Django 4.0.6 on 2023-04-18 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_transaction_fullname_alter_transaction_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='user',
            new_name='customer',
        ),
    ]