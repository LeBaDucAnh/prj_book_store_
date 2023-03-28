# from django.shortcuts import render
# from core.models import *
# from core.serializers import *
# from rest_framework import generics
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.http import HttpResponse
from rest_framework.exceptions import AuthenticationFailed,ValidationError
import jwt,datetime
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import authtoken
import json
class UserRegistration(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token": authtoken.objects.create(user)[1]
        })
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             # Create a new User with the validated data
#             user = User.objects.create_user(
#                 serializer.validated_data['username'],
#                 serializer.validated_data['email'],
#                 serializer.validated_data['password']
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class UserRegistration(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             # Create a new User with the validated data
#             user = User.objects.create_user(
#                 serializer.validated_data['username'],
#                 serializer.validated_data['email'],
#                 serializer.validated_data['password']
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RegisterView(APIView):
#    def post(self, request):
#        username = request.data.get('username')
#        email = request.data.get('email')
#        password = request.data.get('password')
#        if User.objects.filter(username=username).exists():
#            return Response({'message': 'Username already exists'})
#        elif User.objects.filter(email=email).exists():
#            return Response({'message': 'Email already exists'})
#        else:
#            user = User.objects.create_user(username=username, email=email, password=password)
#            login(request, user)
#            return Response({'message': 'Registered successfully'}, status=201)


class UserLogin(APIView):
    def post(self, request):
        # email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        #user=User.objects.filter(email=email).first()
        user = authenticate(request, username = username , password=password)

        if user is not None:
            login(request, user)

            return Response({'message': 'Logged in successfully'},tatus=status.HTTP_200_OK)
            # payload={
            #     'id':user.id,
            #     'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            #     'at':datetime.datetime.utcnow()
            # }
            # print(payload)
            # token =jwt.encode(payload,'secret',algorithm='HS256')
            
            # response=Response()
        

            # response.set_cookie(key='jwt',value=token,httponly=True)
            
            
            # user=User.objects.filter(id=payload['id']).first()
            # serializer=UserSerializer(user)

            # response.data = {
            #     'sucess':True,
            #     'message': 'Dang nhap thanh cong',
            #     'jwt':token,
            #     'status': status.HTTP_200_OK,
            #     'data':serializer.data
            # }

            #return response

        # return Response(data = data, status=status.HTTP_401_UNAUTHORIZED)
        return response

class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)



# class AuthView(APIView):
#    permission_classes = [IsAuthenticated]
#    def get(self, request):
#        user = request.user
#        return Response({'username': user.username})

# class LoginView(APIView):
    



# # # Create your views here.
# class UserRegister(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data) 
    
# class UserLogin(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user=User.objects.filter(email=email).first()

#         if user is None :
#             raise AuthenticationFailed({
#                 'sucess': False,
#                 'message':'Tài khoản không tồn tại',
#                 'status': status.HTTP_404_NOT_FOUND
#             })
        
#         if not user.check_password(password):
#             raise AuthenticationFailed({
#                 'sucess': False,
#                 'message':'Sai mật khẩu đăng nhập',
#                 'status': status.HTTP_404_NOT_FOUND
#             })
        
        
#         payload={
#             'id':user.id,
#             'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'at':datetime.datetime.utcnow()
#         }

#         token =jwt.encode(payload,'secret',algorithm='HS256')
        
#         response=Response()
    
#         response.set_cookie(key='jwt',value=token,httponly=True)
        
        
#         user=User.objects.filter(id=payload['id']).first()
#         serializer=UserSerializer(user)

#         response.data = {
#             'sucess':True,
#             'message': 'Dang nhap thanh cong',
#             'jwt':token,
#             'status': status.HTTP_200_OK,
#             'data':serializer.data
#         }

#         return response


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from .serializers import (UserSerializer, UserSerializerWithToken,
#                           AuthIssueTokenSerializer, InitializePasswordSerializer, ChangePasswordSerializer)

# class CreateUserView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# class IssueTokenView(APIView):
#     def post(self, request):
#         serializer = AuthIssueTokenSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.data['email'].lower()
#             password = serializer.data['password']
#             user = authenticate(username=email, password=password)
#             if user:
#                 serializer = UserSerializerWithToken(user)
#                 return Response(serializer.data)
#             else:
#                 return Response({'error': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class InitializePasswordView(APIView):
#     def post(self, request):
#         serializer = InitializePasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             # process password reset request
#             pass
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ChangePasswordView(APIView):
#     def post(self, request):
#         serializer = ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.data['username']
#             password = serializer.data['password']
#             #new_password = serializer.data['new_password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 user.set_password(password)
#                 user.save()
#                 return Response({'success': 'password changed'})
#             else:
#                 return Response({'error': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GetCurrentUserView(APIView):
#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)

# class UpdateCurrentUserView(APIView):
#     def put(self, request):
#         serializer = UserSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # class ChangeCurrentUserPasswordView(APIView):
# #     def post(self, request):
# #         serializer = ChangeCurrentUserPasswordSerializer(data=request.data)
# #         if serializer.is_valid():
# #             user = request.user
# #             current_password = serializer.data['current_password']
# #             new_password = serializer.data['new_password']
# #             if user.check_password(current_password):
# #                 user.set_password(new_password)
# #                 user.save()
# #                 return Response({'success': 'password changed'})
# #             else:
# #                 return Response({'error': 'invalid password'}, status=status.HTTP_400_BAD_REQUEST)
# #         else:
# #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DeleteCurrentUserView(APIView):
#     def delete(self, request):
#         user = request.user
#         user.delete()
#         return Response({'success': 'account deleted'})

# # class ChangeCurrentUserEmailView(APIView):
# #     def post(self, request):
# #         serializer = ChangeCurrentUserEmailSerializer(data=request.data)
# #         if serializer.is_valid():
# #             user = request.user
# #             current_password = serializer.data['current_password']
# #             new_email = serializer.data['new_email'].lower()
# #             if user.check_password(current_password):
# #                 if User.objects.filter(email__iexact=new_email).exists():
# #                     return Response({'error': 'email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                
# #                 user.email = new_email
# #                 user.username = new_email
# #                 user.save()
# #                 return Response({'success': 'email changed'})
# #             else:
# #                 return Response({'error': 'invalid password'}, status=status.HTTP_400_BAD_REQUEST)
# #         else:
# #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
