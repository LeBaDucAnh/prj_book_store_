from rest_framework.serializers import ModelSerializer
from .models import *

class AuthorSerializers(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'