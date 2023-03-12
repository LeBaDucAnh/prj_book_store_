from rest_framework.serializers import ModelSerializer
from .models import *

class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'