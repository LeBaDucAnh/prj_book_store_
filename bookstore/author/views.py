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
def get_all_author(request):   
    authors =  Author.objects.all()   
    if authors:
        result = AuthorSerializers(authors, many = True).data
        return Response({'data': result,'status': status.HTTP_200_OK})
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def add_author(request):
    authors = AuthorSerializers(data = request.data)
    if authors.is_valid():
        authors.save()
        return Response(authors.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

# API sửa thông tin lớp 
@api_view(['PUT']) 
def update_author(request, pk):
    authors = Author.objects.get(pk = pk)
    serializer = AuthorSerializers(authors,data = request.data )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors,status = status.HTTP_404_NOT_FOUND) 
        
#API xóa thông tin lớp  
@api_view(['DELETE'])
def delete_author(request, pk):
    try:
        authors = Author.objects.get(pk=pk)
        authors.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})
    

@api_view(['GET'])
def search_author(request):
    keyword = request.GET.get('keyword','')
    author_list = Author.objects.all()
    if keyword:
        author_list = Author.objects.filter(
            Q(authorname__icontains = keyword)
        )
    total = author_list.count()
    data = AuthorSerializers(author_list, many = True).data
    result = {'total':total, 'data':data}
    return Response(result)