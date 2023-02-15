from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    category_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

