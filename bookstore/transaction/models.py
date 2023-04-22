from django.db import models
from bookstore.const import TRANS_STATUS
from bookshop.models import Customer

# Create your models here.
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, blank=True,null=True)
    status = models.CharField(choices=TRANS_STATUS, blank=True, max_length=20,null=True, default="PENDING")
    amount = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True,null=True)
    phone = models.CharField(max_length=15, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True)
    fullname = models.CharField(max_length=255, null=True)

    @staticmethod
    def get_transaction_by_customer(customer_id):
        return Transaction.objects.filter(customer=customer_id).order_by('-created_at')
    
    @staticmethod
    def get_all_trans(pk):
        return Transaction.objects.filter(id__in=pk)