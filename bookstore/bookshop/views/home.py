from django.shortcuts import render , redirect , HttpResponseRedirect, get_object_or_404
from book.models import *
from category.models import *
from django.views import View
from bookshop.models import *
from order.models import *
from transaction.models import *
from author.models import *
from order.models import *
from django.contrib.auth.hashers import  check_password, make_password
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class Index(View):
    def post(self , request):
        book = request.POST.get('book')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(book)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(book)
                    else:
                        cart[book]  = quantity-1
                else:
                    cart[book]  = quantity+1

            else:
                cart[book] = 1
        else:
            cart = {}
            cart[book] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')

    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    books = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    customer_id = request.session.get('customer')
    if categoryID:
        books = Book.get_all_books_by_categoryid(categoryID)
    else:
        books = Book.get_all_books()

    data = {}
    data['books'] = books
    data['categories'] = categories
    if request.session.get('customer'):
        fullname = Customer.objects.filter(id = customer_id).values('fullname')
        data['customer']  = fullname[0]['fullname']

    return render(request, 'home.html', data)


def basePage(request):
    categories = Category.objects.all()
    data = {}
    data['categories'] = categories
    if request.session.get('customer'):
        customer_id = request.session.get('customer')
        fullname = Customer.objects.filter(id = customer_id).values('fullname')
        data['customer']  = fullname[0]['fullname']

    return render(request, 'base.html', data)

def get_fullname(cus_id):
        return Customer.objects.filter(id = cus_id).values('fullname')

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    print(email, password)
                    return redirect ('homepage')
            else:
                error_message = 'Password is not correct !!'
        else:
            error_message = 'Customer is not exist !!'

        
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('homepage')

class Signup (View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        fullname = postData.get('fullname')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'fullname': fullname,
            'email': email
        }
        error_message = None

        customer = Customer (fullname=fullname,
                             email=email,
                             password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print (fullname, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect ('login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.fullname):
            error_message = "Please Enter your First Name !!"
        elif len (customer.fullname) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Book.get_books_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'books' : products} )

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        note = request.POST.get('note')
        books = Book.get_books_by_id(list(cart.keys()))
        total = 0
        for product in books:
            qty=cart.get(str(product.id))
            unit_price=product.unit_price
            total +=  qty * unit_price
        
        transaction = Transaction(
            customer=Customer(id =customer),
            fullname=get_fullname(customer),
            address=address,
            phone=phone,
            amount= total
        )
        transaction.save()

        order = Order(
            transaction=transaction,
            total_price=total,
            note=note,
        )
        order.save()

        for product in books:
            qty=cart.get(str(product.id))
            unit_price=product.unit_price
            order_detail = Order_detail(
                order=order,
                book=product,
                qty=qty,
                unit_price=unit_price,
            )
            
            order_detail.save()

        request.session['cart'] = {}

        messages.success(request, 'Your order has been placed.')
        return redirect('homepage')
    

class OrderView(View):
    def get(self , request ):
        customer = request.session.get('customer')
        trans = Transaction.get_transaction_by_customer(customer)
        print(trans)
        return render(request , 'orders.html'  , {'transaction' : trans})
    


class AuthorView(View):
    def get(self, request):
        author = Author.get_all_authors()
        return render(request, 'author.html', {'authors': author})
    

def book(request):
    cart = request.session.get('cart')
    query = request.GET.get('q')
    if not cart:
        request.session['cart'] = {}
    books = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    customer_id = request.session.get('customer')
    if categoryID:
        books = Book.get_all_books_by_categoryid(categoryID)
    elif query:
        books = Book.objects.filter(book_name__icontains=query)
    else:
        books = Book.get_all_books()

    data = {}
    data['books'] = books
    data['categories'] = categories
    data['query'] = query
    if request.session.get('customer'):
        fullname = Customer.objects.filter(id = customer_id).values('fullname')
        data['customer']  = fullname[0]['fullname']

    return render(request, 'book.html', data)

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_detail.html', {'book': book})

def get_book_by_category(request, category_id):
    book = Book.get_all_books_by_categoryid(category_id)
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'category_book.html', {"book_cata": book, 'category': category})

def order_detail(request, pk):
    tran = Transaction.objects.get(pk=pk)
    print(tran.id)
    items = Order.get_orders_by_transaction(tran.id)
    print(items)
    id_value = items['id']
    order_detail = Order_detail.get_orders_detail(id_value)
    return render(request, 'order_detail.html', {'tran': tran, 'orders': order_detail})


def order_delete(request, pk):
    transaction = Transaction.objects.get(pk=pk)
    if transaction:
        transaction.delete()
        #transaction.save()
        customer = request.session.get('customer')
        trans = Transaction.get_transaction_by_customer(customer) 
        return render(request, 'orders.html',{'transaction' : trans})
    else:
        return JsonResponse({'status': 'error', 'message': 'Cannot delete undelivered order.'})



def order_cancel(request, pk):
    transaction = Transaction.objects.get(pk=pk)
    if transaction.status == "PENDING":
        transaction.status = "CANCELED"
        transaction.save()
        customer = request.session.get('customer')
        trans = Transaction.get_transaction_by_customer(customer) 
        return render(request, 'orders.html',{'transaction' : trans})
    else:
        return JsonResponse({'status': 'error', 'message': 'Cannot cancel confirmed order.'})
    
        