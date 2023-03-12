from rest_framework.serializers import ModelSerializer
from .models import *

class PublisherSerializers(ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'