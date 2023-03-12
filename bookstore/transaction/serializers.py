from rest_framework.serializers import ModelSerializer
from .models import *

class PaymentSerializers(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class TransactionSerializers(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'