from django.urls import path
from .views import PublisherAPIView

urlpatterns = [
    path('publishers/', PublisherAPIView.as_view()),
    path('publishers/<int:pk>/', PublisherAPIView.as_view()),
]
