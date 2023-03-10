from django.shortcuts import render
from core.models import *
from core.serializers import *
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.exceptions import AuthenticationFailed,ValidationError
import jwt,datetime

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