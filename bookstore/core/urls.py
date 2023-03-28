from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views
# from .views import CreateUserView, IssueTokenView, InitializePasswordView, ChangePasswordView
urlpatterns = [
    path('register/', UserRegistration.as_view(), name="user-registration"),
    # path('userregister/', UserRegister.as_view(), name="user-registration"),
    path('loginuser/', UserLogin.as_view(), name="user-login"),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name="user-login"),
    # path('logout/', UserLogout.as_view(), name="user-logout"),
    # path('users/', CreateUserView.as_view()),
    # path('auth/token/', IssueTokenView.as_view()),
    # path('auth/initialize-password/', InitializePasswordView.as_view()),
    # path('auth/change-password/', ChangePasswordView.as_view())
]



