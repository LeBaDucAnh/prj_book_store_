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
def get_all_publisher(request):   
    publishers =  Publisher.objects.all()   
    if publishers:
        result = PublisherSerializers(publishers, many = True).data
        return Response({'data': result,'status': status.HTTP_200_OK})
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def add_publisher(request):
    publishers = PublisherSerializers(data = request.data)
    if publishers.is_valid():
        publishers.save()
        return Response(publishers.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

# API sửa thông tin 
@api_view(['PUT']) 
def update_publisher(request, pk):
    publishers = Publisher.objects.get(pk = pk)
    serializer = PublisherSerializers(publishers,data = request.data )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors,status = status.HTTP_404_NOT_FOUND) 
        
#API xóa thông tin  
@api_view(['DELETE'])
def delete_publisher(request, pk):
    try:
        publishers = Publisher.objects.get(pk=pk)
        publishers.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})
    

@api_view(['GET'])
def search_publisher(request):
    keyword = request.GET.get('keyword','')
    publisher_list = Publisher.objects.all()
    if keyword:
        publisher_list = Publisher.objects.filter(
            Q(authorname__icontains = keyword)
        )
    total = publisher_list.count()
    data = PublisherSerializers(publisher_list, many = True).data
    result = {'total':total, 'data':data}
    return Response(result)