from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Cart, Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Home Page - List all books
def book_list(request):
    books = Book.objects.all()
    return render(request, 'store/book_list.html', {'books': books})

# Book Details Page
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'store/book_detail.html', {'book': book})

# Add to Cart
@login_required
def add_to_cart(request, id):
    book = get_object_or_404(Book, id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

# View Cart
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

# Checkout
@login_required
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        cart_items = Cart.objects.filter(user=request.user)
        total = sum(item.book.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_amount=total, address=address)
        
        for item in cart_items:
            OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity, price=item.book.price)
        cart_items.delete()
        return redirect('order_success')
    
    return render(request, 'store/checkout.html')

# Order Success Page
@login_required
def order_success(request):
    return render(request, 'store/order_success.html')

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('book_list')
    return render(request, 'store/login.html')

# Signup
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('book_list')
    return render(request, 'store/signup.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('book_list')
