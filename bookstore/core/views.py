from rest_framework.exceptions import AuthenticationFailed,ValidationError
import jwt,datetime
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import authtoken
import json
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes

@permission_classes([IsAuthenticated])
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': "Register successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogin(APIView):
    def post(self, request):
        password = request.data.get('password')
        username = request.data.get('username')
        user = authenticate(request, username = username , password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            #login(request, user)
            return Response({'message': 'Logged in successfully', 'token':token.key},status=status.HTTP_200_OK)


class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)