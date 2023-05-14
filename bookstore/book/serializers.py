from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from category.serializers import CategorySerializer
from author.serializers import AuthorSerializer

class BookSerializer(ModelSerializer):
    #image = serializers.SerializerMethodField()
    author = AuthorSerializer(required = False)
    category = CategorySerializer(required = False)
    class Meta:
        model = Book
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        if request is not None:
            return request.build_absolute_uri(image_url)
        return image_url