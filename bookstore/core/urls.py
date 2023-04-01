from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name="user-registration"),
    path('loginuser/', UserLogin.as_view(), name="user-login"),
    path('loginadmin/', jwt_views.TokenObtainPairView.as_view(), name="user-login"),
    path('change-password/', ChangePasswordView.as_view()),
    path('profile/', ProfileView.as_view()),
]