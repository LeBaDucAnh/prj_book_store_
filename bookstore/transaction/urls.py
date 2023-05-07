from django.urls import path
from .views import *

urlpatterns = [
    path('transactions/', TransactionList.as_view()),
    path('transaction/<int:pk>/', TransactionDetail.as_view()),
    path('order_statistics/', order_statistics.as_view()),
    path('daily-revenue/', DailyRevenue.as_view()),
]

