from django.contrib import admin
from django.urls import path
from .views.home import *
from .middlewares.auth import auth_middleware
from .views.customer_views import *
from django.contrib.auth import views as auth_views



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
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('profile', view_profile, name='profile'),
    path('edit-profile', edit_profile, name='edit_profile'),
    path('change-password', change_password, name='change_password'),
]