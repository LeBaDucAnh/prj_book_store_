from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import VoucherList, VoucherDetailDetail

urlpatterns = [
    path('voucher_details/', VoucherList.as_view()),
    path('voucher_details/<int:pk>/', VoucherDetailDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
