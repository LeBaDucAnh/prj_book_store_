from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer
from datetime import timezone
from django.http import Http404
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from django.db.models.functions import TruncDay
from django.db.models import Sum
class TransactionList(APIView):
    def get(self, request, format=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            voucher = serializer.validated_data['voucher']
            payment = serializer.validated_data['payment']
            # Check if the voucher is valid
            if voucher.user != user:
                return Response({'error': 'Voucher does not belong to user.'}, status=status.HTTP_400_BAD_REQUEST)
            if voucher.start_date > timezone.now() or voucher.end_date < timezone.now() or voucher.qty <= 0:
                return Response({'error': 'Voucher is invalid or out of stock.'}, status=status.HTTP_400_BAD_REQUEST)
            # Create the transaction
            transaction = serializer.save()
            # Redeem the voucher
            voucher_detail = voucher.voucher_detail_set.filter(user=user, start_date__lte=timezone.now(), end_date__gte=timezone.now(), qty__gt=0).first()
            if voucher_detail:
                voucher_detail.qty -= 1
                voucher_detail.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetail(APIView):
    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class order_statistics(APIView):
    def get(self, request):
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=30)
        confirmed_orders = Transaction.objects.filter(status='PENDING', created_at__gte=start_date, created_at__lte=end_date).count()
        shipping_orders = Transaction.objects.filter(status='DELIVERING', created_at__gte=start_date, created_at__lte=end_date).count()
        delivered_orders = Transaction.objects.filter(status='COMPLETED', created_at__gte=start_date, created_at__lte=end_date).count()
        canceled_orders = Transaction.objects.filter(status='CANCELED', created_at__gte=start_date, created_at__lte=end_date).count()
        data = {
            'labels': ['Chờ xác nhận', 'Đang giao', 'Đã giao', 'Đã hủy'],
            'values': [confirmed_orders, shipping_orders, delivered_orders, canceled_orders],
        }
        return Response(data)
    
class DailyRevenue(APIView):
    def get(self, request):
        daily_revenue = Transaction.objects.filter(status='COMPLETED').annotate(day=TruncDay('updated_at')).values('day').annotate(revenue=Sum('amount')).order_by('day')
        print(daily_revenue)
        data = [
            { 'day': order['day'].strftime('%d/%m/%Y'), 'revenue': float(order['revenue']) } 
            for order in daily_revenue
        ]
        return Response(data)