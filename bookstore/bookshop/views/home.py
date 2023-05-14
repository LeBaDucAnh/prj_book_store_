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
from django import forms
from review.models import *
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def cart_product(self , request):
        ids = list(request.session.get('cart').keys())
        products = Book.get_books_by_id(ids)
        print(products)
        return render(request , 'cart.html' ,  {'books' : products})
class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Book.get_books_by_id(ids)
        print(products)
        return render(request , 'cart.html' ,  {'books' : products})
        #return HttpResponseRedirect(f'/cả{request.get_full_path()[1:]}', )
    
    def post(self , request):
        book = request.POST.get('book')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        dele = request.POST.get('del')
        if cart:
            quantity = cart.get(book)
            if quantity:
                if not remove:
                    cart[book] = quantity+1
                else:
                    if quantity<=1:
                        cart.pop(book)
                    elif dele:
                        cart.pop(book)
                    else:
                        cart[book]  = quantity-1
            # else:
            #     cart[book] = 1
        else:
            cart = {}
            cart[book] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        print(book)
        return redirect('cart')
        #return HttpResponseRedirect(f'{request.get_full_path()[1:]}')

    # def delete(self, request):
    #     book = request.POST.get('book')
    #     cart = request.session.get('cart')
    #     quantity = cart.get(book)
    #     if cart:
    #         cart.pop(book)
    #         del cart[book]
        
    #     request.session['cart'] = cart
    #     return redirect('cart')

    # def get(self , request):
    #     # print()
    #     return HttpResponseRedirect(f'{request.get_full_path()[1:]}')

# def update_quantity(request):
#     item_id = request.POST.get('item_id')
#     quantity = request.POST.get('quantity')
#     cart = Cart(request)
#     cart.update(item_id, int(quantity))
#     cart_items = cart.get_items()
#     context = {'cart_items': cart_items}
#     return render(request, 'cart.html', context)

class Index(View):
    def post(self , request):
        book = request.POST.get('book')
        qty = request.POST.get('qty_book')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        print('so luong: ',qty)
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
            bookss = Book.objects.get(id = product.id)
            bookss.qty -= qty
            bookss.save()
    
        transaction = Transaction(
            customer=Customer(id =customer),
            fullname=get_fullname(customer),
            address=address,
            phone=phone,
            amount= total,
            message = note,
        )
        transaction.save()

        order = Order(
            transaction=transaction,
            total_price=total,
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

        messages.success(request, 'Đặt hàng thành công.')
        return redirect('homepage')
    

class OrderView(View):
    def get(self , request ):
        customer = request.session.get('customer')
        trans = Transaction.get_transaction_by_customer(customer)
        print(trans)
        return render(request , 'orders.html'  , {'transaction' : trans})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['star', 'comment']
    CHOICES = [(1, '1 sao'), (2, '2 sao'), (3, '3 sao'), (4, '4 sao'), (5, '5 sao')]
    star = forms.ChoiceField(label="Số sao đánh giá", choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'star'}))
    #star = forms.IntegerField(label="Số sao đánh giá")
    comment = forms.CharField(label="Bình luận", widget=forms.Textarea(attrs={'rows': 3}))
    #     widgets = {
    #         'comment': forms.Textarea(attrs={'rows': 3})
    #     }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['star'].widget.attrs['class'] = 'rating-widget'


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
    comments = book.reviews.all()
    if request.session.get('customer'):
        customer_id = request.session.get('customer')
        customer = get_object_or_404(Customer, pk = customer_id)
        fullname = Customer.objects.filter(id = customer_id).values('fullname')
        # data['customer']  = fullname[0]['fullname']
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            comment.customer = customer
            comment.book = book
            comment.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = CommentForm()
    data = [1, 2, 3, 4, 5]
    return render(request, 'book_detail.html', {'book': book,'comments': comments, 'form': form, 'stars': data})

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
        print(transaction) 
        print(transaction.id)
        items = Order.get_orders_by_transaction(transaction.id)
        print(items)
        id_value = items['id']
        order_detail = Order_detail.get_orders_detail(id_value)
        for order in order_detail:
            print(order.book.id)
            book = Book.objects.get(pk = order.book.id)
            book.qty += order.qty
            book.save()
        return render(request, 'orders.html',{'transaction' : trans})
    else:
        return JsonResponse({'status': 'error', 'message': 'Cannot cancel confirmed order.'})
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(email)
            try:
                user = Customer.objects.get(email=email)
                print(user)
            except Customer.DoesNotExist:
                user = None
            if user is not None:
                form = PasswordResetForm({'email': email})
                if form.is_valid():
                    form.save(
                        request=request,
                        use_https=request.is_secure(),
                        subject_template_name='registration/password_reset_subject.txt',
                        email_template_name='registration/password_reset_email.html',
                        html_email_template_name='registration/password_reset_email.html',
                    )
                    return HttpResponseRedirect(reverse('password_reset_done'))
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})



def update_quantity(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        qty = request.POST.get('qty')
        # Cập nhật số lượng cần mua
        # ...
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['fullname', 'email']

def edit_profile(request):
    customer_id = request.session.get('customer')
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            # Lưu thông tin cá nhân của khách hàng
            form.save()
            # và chuyển hướng đến trang thông tin cá nhân
            return redirect('profile')
    else:
        # Hiển thị form để cho khách hàng cập nhật thông tin cá nhân
        form = CustomerForm(instance=customer)
    return render(request, 'edit_info.html', {'form': form})

def view_profile(request):
    customer_id = request.session.get('customer')
    customer = Customer.objects.get(id=customer_id)
    return render(request, 'profile.html', {'customer': customer})

class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Mật khẩu hiện tại',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu hiện tại'}))
    new_password1 = forms.CharField(label='Mật khẩu mới',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu mới'}))
    new_password2 = forms.CharField(label='Xác nhận mật khẩu',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu mới'}))

def change_password(request):
    if request.method == 'POST':
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(id = customer_id)
        print(customer_id)
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            confirm_new_password = form.cleaned_data['new_password2']
            print(confirm_new_password)
            if check_password(current_password, customer.password):
                if new_password == confirm_new_password:
                    #request.customer.set_password(new_password)
                    hashed_password = make_password(new_password)
                    customer.password = hashed_password
                    customer.save()
                    messages.success(request, 'Mật khẩu của bạn đã được thay đổi thành công.')
                    return redirect('profile')
            else:
                messages.error(request, "Có lỗi khi đổi")
        # form = CustomPasswordChangeForm(customer_id, request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     update_session_auth_hash(request, user)
        #     messages.success(request, 'Mật khẩu đã được thay đổi thành công.')
        #     return redirect('profile')
        else:
            messages.error(request, 'Vui lòng sửa các lỗi bên dưới.')
    else:
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(id=customer_id)
        form = CustomPasswordChangeForm(initial={'customer': customer})
    return render(request, 'change_pass.html', {'form': form})