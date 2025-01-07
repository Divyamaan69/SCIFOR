from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Book
from .cart import Cart

def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.add(book=book)
    return redirect('cart_detail')

def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

# def checkout(request):
#     cart = Cart(request)
#     return render(request, 'cart/checkout.html', {'cart': cart})

from django.shortcuts import render, redirect
from store.models import Order, OrderItem
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')  # Redirect if the cart is empty

    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method', 'COD')

        order = Order.objects.create(
            user=request.user,
            total_price=sum(item['price'] * item['quantity'] for item in cart.values()),
            address=address,
            payment_method=payment_method
        )

        for book_id, item in cart.items():
            OrderItem.objects.create(
                order=order,
                book_id=book_id,
                quantity=item['quantity'],
                price=item['price']
            )

        # Clear cart after placing the order
        del request.session['cart']
        return redirect('order_success')

    return render(request, 'cart/checkout.html')
