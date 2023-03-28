from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('transactions/', TransactionList.as_view()),
    path('transactions/<int:pk>/', TransactionDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
