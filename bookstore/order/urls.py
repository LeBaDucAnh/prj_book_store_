from django.urls import path
from .views import OrderList, OrderDetail, OrderDetailList, OrderDetailDetail, add_to_cart, checkout, GetAllOrderProduct, GetAllOrderDetail, report

urlpatterns = [
    path('orders/', OrderList.as_view()),
    path('orders/<int:pk>/', OrderDetail.as_view()),
    path('order-details/', OrderDetailList.as_view()),
    path('order-details/<int:pk>/', OrderDetailDetail.as_view()),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-trans/<int:pk>/', GetAllOrderProduct.as_view()),
    path('detail/<int:pk>/', GetAllOrderDetail.as_view()),
    path('report/', report),
]

