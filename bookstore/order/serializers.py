from rest_framework.serializers import ModelSerializer
from .models import *

class StatusSerializers(ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class OderSerializers(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OderDetailSerializers(ModelSerializer):
    class Meta:
        model = Order_detail
        fields = '__all__'