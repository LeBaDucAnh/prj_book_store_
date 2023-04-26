from django.contrib import admin
from django.urls import path
from .views.home import *
from .middlewares.auth import auth_middleware
from .views.customer_views import *

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('author', AuthorView.as_view(), name="author"),
    path('book', book, name='book'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('category/<int:category_id>/', get_book_by_category),
    path('orders/<int:pk>/cancel/', order_cancel, name='order_cancel'),
    path('orders/<int:pk>/delete/', order_delete, name='order_delete'),
    path('order-detail/<int:pk>', order_detail, name="order_detail"),
    path('customers/', CustomerList.as_view(), name='customer-list'),
    path('customer/<int:pk>/', CustomerDetail.as_view(), name="customer-detail"),
]