from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class AuthorSerializer(ModelSerializer):
    author_image = serializers.SerializerMethodField()
    class Meta:
        model = Author
        fields = '__all__'

    def get_author_image(self, obj):
        request = self.context.get('request')
        image_url = obj.author_image.url
        if request is not None:
            return request.build_absolute_uri(image_url)
        return image_url