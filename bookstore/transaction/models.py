from django.db import models
from bookstore.const import TRANS_STATUS
from core.models import User

# Create your models here.
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, blank=True,null=True)
    status = models.CharField(choices=TRANS_STATUS, blank=True, max_length=20,null=True)
    amount = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True,null=True)
    phone = models.CharField(max_length=15, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    fullname = models.CharField(max_length=255, null=True)

