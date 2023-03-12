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
def get_all_category(request):   
    categorys =  Category.objects.all()   
    if categorys:
        result = CategorySerializers(categorys, many = True).data
        return Response({'data': result,'status': status.HTTP_200_OK})
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def add_category(request):
    categorys = CategorySerializers(data = request.data)
    if categorys.is_valid():
        categorys.save()
        return Response(categorys.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

# API sửa thông tin 
@api_view(['PUT']) 
def update_category(request, pk):
    categorys = Category.objects.get(pk = pk)
    serializer = CategorySerializers(categorys,data = request.data )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors,status = status.HTTP_404_NOT_FOUND) 
        
#API xóa thông tin  
@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        categorys = Category.objects.get(pk=pk)
        categorys.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})
    

@api_view(['GET'])
def search_category(request):
    keyword = request.GET.get('keyword','')
    category_list = Category.objects.all()
    if keyword:
        category_list = Category.objects.filter(
            Q(authorname__icontains = keyword)
        )
    total = category_list.count()
    data = CategorySerializers(category_list, many = True).data
    result = {'total':total, 'data':data}
    return Response(result)