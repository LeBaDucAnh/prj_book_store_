from django.shortcuts import render
from core.models import *
from core.serializers import *
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.exceptions import AuthenticationFailed,ValidationError
import datetime, jwt


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer

class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new User with the validated data
            user = User.objects.create_user(
                serializer.validated_data['username'],
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        
        serializer=UserSerializer(user)

        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'at':datetime.datetime.utcnow()
        }

        token =jwt.encode(payload,'secret',algorithm='HS256')
        response=Response()
    
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'sucess':True,
            'message': 'Dang nhap thanh cong',
            'jwt':token,
            'status': status.HTTP_200_OK,
            'data':serializer.data
        }

        # return Response(data = data, status=status.HTTP_401_UNAUTHORIZED)
        return response

class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)









# Create your views here.
class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 
    
class UserLogin(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user=User.objects.filter(email=email).first()

        if user is None :
            raise AuthenticationFailed({
                'sucess': False,
                'message':'Tài khoản không tồn tại',
                'status': status.HTTP_404_NOT_FOUND
            })
        
        if not user.check_password(password):
            raise AuthenticationFailed({
                'sucess': False,
                'message':'Sai mật khẩu đăng nhập',
                'status': status.HTTP_404_NOT_FOUND
            })
        
        
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'at':datetime.datetime.utcnow()
        }

        token =jwt.encode(payload,'secret',algorithm='HS256')
        
        response=Response()
    
        response.set_cookie(key='jwt',value=token,httponly=True)
        
        
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSerializer(user)

        response.data = {
            'sucess':True,
            'message': 'Dang nhap thanh cong',
            'jwt':token,
            'status': status.HTTP_200_OK,
            'data':serializer.data
        }

        return response