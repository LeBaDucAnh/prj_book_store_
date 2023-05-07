from django.db import models
from transaction.models import Transaction
from book.models import Book

# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True)
    total_price = models.IntegerField(blank=True)
    note = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_transaction(trans_id):
        return Order.objects.filter(transaction=trans_id).values('id').first()

class Order_detail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, related_name='order_detail')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    qty = models.IntegerField(blank=True)
    unit_price = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_orders_detail(order_id):
        return Order_detail.objects.filter(order=order_id)