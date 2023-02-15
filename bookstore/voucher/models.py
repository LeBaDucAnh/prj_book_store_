from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Voucher(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=6, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Voucher_detail(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    discount = models.IntegerField(blank=True)
    qty = models.IntegerField(blank=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)