from django.db import models
from transaction.models import Transaction
from book.models import Book

# Create your models here.
class Status(models.Model):
    id = models.AutoField(primary_key=True)
    status_value = models.CharField(max_length=255)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True)
    price = models.IntegerField(blank=True)
    note = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_detail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    qty = models.IntegerField(blank=True)
    unit_price = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_history(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)
    status_date = models.DateTimeField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True)