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
import bcrypt
from django.contrib.auth.hashers import check_password

#@permission_classes([IsAuthenticated])
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
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'detail': 'Email or password is missing'}, status=status.HTTP_400_BAD_REQUEST)
        print(email)
        print(password)
        user = User.objects.filter(email=email).first()
        print(user.id)
        #user = authenticate(email=email, password=password)
        if check_password(password, user.password):
            login(request, user)
            token, _ = Token.objects.get_or_create(user_id=user.id)
            print(token.__dict__)
            return Response(data = {'message': 'Logged in successfully', 'token': token.key, 'user': user.email}, status=status.HTTP_200_OK)
        else:
            # Trả về thông báo lỗi không thể đăng nhập
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
# def post(self, request):
    #     password = request.data.get('password')
    #     email = request.data.get('email')
    #     user = authenticate(request, username = email , password=password)

    #     if user is not None:
    #         #token, created = Token.objects.get_or_create(user=user), 'token':token.key
    #         #login(request, user)
    #         token, _ = Token.objects.get_or_create(user=user)
    #         #return Response({})'message': 'Logged in successfully', 
    #         return Response({'token': token.key},status=status.HTTP_200_OK)
class LoginAdminView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if check_password(password, user.password) and user.is_admin:
            login(request, user)
            return Response({'detail': 'Logged in successfully.'})
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


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
        

from django.contrib.auth import get_user_model
class AdminRegister(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        User = get_user_model()
        admin_user = User.objects.create_superuser(email=email, password=password)
        return Response(status=status.HTTP_200_OK)