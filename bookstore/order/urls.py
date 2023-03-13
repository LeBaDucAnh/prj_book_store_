from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import OrderList, OrderDetail, OrderDetailList, OrderDetailDetail, OrderHistoryList, OrderHistoryDetail

urlpatterns = [
    path('orders/', OrderList.as_view()),
    path('orders/<int:pk>/', OrderDetail.as_view()),
    path('order-details/', OrderDetailList.as_view()),
    path('order-details/<int:pk>/', OrderDetailDetail.as_view()),
    path('order-histories/', OrderHistoryList.as_view()),
    path('order-histories/<int:pk>/', OrderHistoryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
