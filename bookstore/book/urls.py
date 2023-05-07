from django.urls import path
from .views import BookList, BookDetail, BookRetrive, BookStats

urlpatterns = [
    path('books/', BookList.as_view()),
    path('book/<int:pk>/', BookRetrive.as_view()),
    path('books/<int:pk>/', BookDetail.as_view()),
    path('product-stats/', BookStats.as_view()),
]
