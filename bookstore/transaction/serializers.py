from rest_framework.serializers import ModelSerializer
from .models import *


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'