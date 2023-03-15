from django.urls import path
from .views import *
from .views import CreateUserView, IssueTokenView, InitializePasswordView, ChangePasswordView
urlpatterns = [
    # path('api/register/', UserRegistration.as_view(), name="user-registration"),
    # path('api/login/', UserLogin.as_view(), name="user-login"),
    # path('api/logout/', UserLogout.as_view(), name="user-logout"),
    path('users/', CreateUserView.as_view()),
    path('auth/token/', IssueTokenView.as_view()),
    path('auth/initialize-password/', InitializePasswordView.as_view()),
    path('auth/change-password/', ChangePasswordView.as_view())
]



