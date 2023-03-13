from django.db import models
from django.contrib.auth.models import User
from book.models import Book

# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(blank=True)
    message = models.TextField(max_length=2000, blank=True)
    image = models.ImageField(upload_to='reviews/')
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)


# class Review_book(models.Model):
#     id = models.AutoField(primary_key=True)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
#     review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
#     comment = models.TextField(max_length=1000, blank=True)
#     image = models.ImageField(upload_to='reviews/')


# class User_review(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
