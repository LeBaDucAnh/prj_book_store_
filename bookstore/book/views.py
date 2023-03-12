from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q

# Create your views here.
@api_view(['GET'])
def get_all_book(request):   
    books =  Book.objects.all()   
    if books:
        result = BookSerializers(books, many = True).data
        return Response({'data': result,'status': status.HTTP_200_OK})
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def add_book(request):
    books = BookSerializers(data = request.data)
    if books.is_valid():
        books.save()
        return Response(books.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

# API sửa thông tin 
@api_view(['PUT']) 
def update_book(request, pk):
    books = Book.objects.get(pk = pk)
    serializer = BookSerializers(books,data = request.data )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors,status = status.HTTP_404_NOT_FOUND) 
        
#API xóa thông tin  
@api_view(['DELETE'])
def delete_book(request, pk):
    try:
        books = Book.objects.get(pk=pk)
        books.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})
    

@api_view(['GET'])
def search_book(request):
    keyword = request.GET.get('keyword','')
    book_list = Book.objects.all()
    if keyword:
        book_list = Book.objects.filter(
            Q(authorname__icontains = keyword)
        )
    total = book_list.count()
    data = BookSerializers(book_list, many = True).data
    result = {'total':total, 'data':data}
    return Response(result)