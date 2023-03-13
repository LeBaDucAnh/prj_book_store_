from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PaymentList, PaymentDetail

urlpatterns = [
    path('payments/', PaymentList.as_view()),
    path('payments/<int:pk>/', PaymentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
