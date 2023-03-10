from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate")
        return lower_email

    class Meta:
        model = User
        fields = ('token', 'username', 'email', 'password')

class AuthIssueTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)


class InitializePasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    session = serializers.CharField(max_length=2048)
    reset_password = serializers.CharField(max_length=255)


class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
