from rest_framework.serializers import ModelSerializer
from .models import *

class PublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'