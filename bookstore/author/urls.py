from django.urls import path
from .views import AuthorList, AuthorDetail, AuthorRetriew

urlpatterns = [
    path('authors/', AuthorList.as_view()),
    path('author/<int:pk>/', AuthorRetriew.as_view()),
    path('authors/<int:pk>/', AuthorDetail.as_view()),
]
