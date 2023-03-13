from rest_framework.serializers import ModelSerializer
from .models import *

class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = Order_detail
        fields = '__all__'

class OrderHistorySerializer(ModelSerializer):
    class Meta:
        model = Order_history
        fields = '__all__'