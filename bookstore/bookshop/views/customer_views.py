from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bookshop.models import Customer
from bookshop.serializers import CustomerSerializer
from django.http import Http404

class CustomerList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        Customer = self.get_object(pk)
        serializer = CustomerSerializer(Customer)
        return Response(serializer.data)

    def put(self, request, pk):
        Customer = self.get_object(pk)
        serializer = CustomerSerializer(Customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Customer = self.get_object(pk)
        Customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
