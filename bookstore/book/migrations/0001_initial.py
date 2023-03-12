# Generated by Django 4.1.7 on 2023-03-03 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
        ('category', '__first__'),
        ('publisher', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('book_name', models.CharField(blank=True, max_length=255)),
                ('dimensions', models.CharField(blank=True, max_length=255)),
                ('pages', models.IntegerField(blank=True)),
                ('publication_date', models.DateField(blank=True)),
                ('language', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True, max_length=2000)),
                ('price', models.IntegerField(blank=True)),
                ('status', models.CharField(choices=[('IN STOCK', 'IN STOCK'), ('OUT OF STOCK', 'OUT OF STOCK')], default='IN STOCK', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('qty', models.IntegerField(blank=True)),
                ('total_qty', models.IntegerField(blank=True)),
                ('image', models.ImageField(upload_to='books/')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='author.author')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='publisher.publisher')),
            ],
        ),
    ]
