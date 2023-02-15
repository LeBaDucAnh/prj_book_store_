from django.db import models
from bookstore.const import TRANS_STATUS
from django.contrib.auth.models import User
from voucher.models import Voucher

# Create your models here.
class Payment(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    payment_name = models.CharField(max_length=255, blank=True)
    payment_info = models.CharField(max_length=255, blank=True)


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, blank=True)
    status = models.CharField(choices=TRANS_STATUS, blank=True, max_length=20)
    amount = models.IntegerField(blank=True)
    message = models.CharField(max_length=255, blank=True)
    security_code = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True)

