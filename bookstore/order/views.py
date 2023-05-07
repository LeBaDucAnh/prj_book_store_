from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import datetime
from rest_framework.decorators import api_view
from book.models import Book
from django.http import JsonResponse

class OrderList(APIView):
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    
    def post(self, request,format=None):
        # book_id = self.request.get('book_id')
        # product = self.get_object_or_404(Book, pk=book_id)
        # cart = request.session.get('cart', {})
        # if book_id not in cart:
        #     cart[book_id] = {
        #         'name': product.name,
        #         'price': float(product.price),
        #         'quantity': 1,
        #     }
        # else:
        #     cart[book_id]['quantity'] += 1
        # request.session['cart'] = cart
        # return Response({'success': True}, status=status.HTTP_201_CREATED)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetAllOrderProduct(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(transaction=pk)
        except Order.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        order_detail = self.get_object(pk)
        serializer = OrderSerializer(order_detail)
        return Response(serializer.data)

class GetAllOrderDetail(APIView):
    def get_object(self, pk):
        try:
            return Order_detail.objects.filter(order=pk).values()
        except Order_detail.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
            order_details = order.order_detail.all()
            serializer = OrderDetailSerializer(order_details, many=True)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class OrderDetailList(APIView):
    def get(self, request):
        order_details = Order_detail.objects.all()
        serializer = OrderDetailSerializer(order_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailDetail(APIView):
    def get_object(self, pk):
        try:
            return Order_detail.objects.get(pk=pk)
        except Order_detail.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        order_detail = self.get_object(pk)
        serializer = OrderDetailSerializer(order_detail)
        return Response(serializer.data)

    def put(self, request, pk):
        order_detail = self.get_object(pk)
        serializer = OrderDetailSerializer(order_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order_detail = self.get_object(pk)
        order_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class OrderHistoryList(APIView):
#     def get(self, request):
#         order_histories = Order_history.objects.all()
#         serializer = OrderHistorySerializer(order_histories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = OrderHistorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class OrderHistoryDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Order_history.objects.get(pk=pk)
#         except Order_history.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         order_history = self.get_object(pk)
#         serializer = OrderHistorySerializer(order_history)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         order_history = self.get_object(pk)
#         serializer = OrderHistorySerializer(order_history, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         order_history = self.get_object(pk)
#         order_history.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['POST'])
def add_to_cart(request, pk):
    # Kiểm tra xem sản phẩm có tồn tại hay không
    book = get_object_or_404(Book, id=pk)

    # Lấy giỏ hàng hiện tại của người dùng từ session
    cart = request.session.get('cart', {})

    # Kiểm tra xem sản phẩm có đã có trong giỏ hàng hay chưa
    if pk in cart:
        # Nếu sản phẩm đã có trong giỏ hàng,
        # tăng số lượng sản phẩm lên 1
        cart[pk]['quantity'] += 1
    else:
        # Nếu sản phẩm chưa có trong giỏ hàng,
        # thêm mới sản phẩm vào giỏ hàng
        cart[pk] = {
            'book_name': book.book_name,
            'price': book.price,
            'qty': 1
        }

    # Lưu lại giỏ hàng mới vào session
    request.session['cart'] = cart

    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    # Lấy giỏ hàng hiện tại của người dùng từ session
    cart = request.session.get('cart', {})

    if cart:
        # Tạo đối tượng Transaction
        transaction = Transaction.objects.create(
            user=request.user
        )
        transaction.save()

        # Tạo đối tượng Order
        order = Order.objects.create(
            transaction=transaction,
            price=sum(item['price'] * item['qty'] for item in cart.values()),
            note=''
        )
        order.save()

        # Lưu thông tin chi tiết đơn hàng
        for book_id, item in cart.items():
            book = get_object_or_404(Book, id=book_id)
            order_detail = Order_detail.objects.create(
                order=order,
                book=book,
                qty=item['qty'],
                unit_price=item['price']
            )
            order_detail.save()

        # Lưu thông tin lịch sử đơn hàng
        # status = get_object_or_404(Status, status_value='Đã thanh toán')
        # order_history = Order_history.objects.create(
        #     order=order,
        #     status_date=datetime.now(),
        #     status=status
        # )
        # order_history.save()

        # Xóa giỏ hàng trong session
        request.session['cart'] = {}

        # Trả về kết quả thành công
        return Response({'success': True})
    else:
        # Nếu giỏ hàng trống, trả về thông báo lỗi
        return Response({'success': False, 'error': 'Cart is empty'})


def report(request):
    # Lấy danh sách sách trong kho
    books = Book.objects.all()
    book_data = [{'title': book.book_name, 'quantity': book.qty} for book in books]

    # Lấy danh sách đơn hàng trong ngày hôm nay
    today = datetime.date.today()
    orders = Transaction.objects.filter(updated_at__date=today, status='COMPLETED')
    revenue = sum([order.amount for order in orders])

    # Trả về dữ liệu dưới dạng JSON
    data = {
        'revenue': revenue,
        'books': book_data,
    }
    return JsonResponse(data)