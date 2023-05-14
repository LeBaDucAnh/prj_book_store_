from django.db import models
from bookshop.models import Customer
from book.models import Book

# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    book_name = models.CharField(max_length=255, null=True)
    fullname = models.CharField(max_length=255, null=True)
    star = models.IntegerField(blank=True)
    comment = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

