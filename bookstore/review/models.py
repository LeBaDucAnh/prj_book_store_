from django.db import models
from core.models import User
from book.models import Book

# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book_name = models.CharField(max_length=255, null=True)
    fullname = models.CharField(max_length=255, null=True)
    star = models.IntegerField(blank=True)
    comment = models.TextField(max_length=2000, blank=True)
    image = models.ImageField(upload_to='reviews/')
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)

