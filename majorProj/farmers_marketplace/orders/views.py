from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Order
from products.models import Product
from .forms import CheckoutForm
import razorpay

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Cart, Order, OrderItem
from django.http import JsonResponse, HttpResponse

@login_required
def place_order(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Get cart items
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = cart.cart_items.all() if cart else []
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        if not cart_items:
            return redirect('view_cart')

        # Create the order
        order = Order.objects.create(
            buyer=request.user,
            total_price=total_price,
            status='CONFIRMED',
        )

        # Add items to order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )

        # Clear the cart
        cart.cart_items.all().delete()

        # Send confirmation email
        subject = "Order Confirmation"
        message = f"Your order is confirmed!\n\nAddress: {address}\nPhone: {phone}\nEmail: {email}\nTotal Amount: Rs. {total_price}\n\nKeep your cash ready. Thank you for shopping with us!"
        send_mail(
                'Order Confirmation',
                f'Your order has been placed. Total amount: Rs. {total_price}. Keep your cash ready!',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,  # Ensure errors raise exceptions
                )

        return render(request, 'orders/order_confirmation.html', {'order': order, 'address': address, 'phone': phone, 'email': email, 'total_price': total_price})

    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.cart_items.all() if cart else []
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'orders/place_order.html', {'cart_items': cart_items, 'total_price': total_price})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-timestamp')
    return render(request, 'orders/order_history.html', {'orders': orders})

from django.shortcuts import get_object_or_404, redirect
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# orders/views.py

from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # If it's already in the cart, update the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('orders:view_cart')


from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def view_cart(request):
    # Get the user's cart (or create one if it doesn't exist)
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        cart = Cart.objects.create(user=request.user)  # Create a cart if it doesn't exist

    # Get the items in the cart
    cart_items = cart.cart_items.all()
    
    # Calculate the total price
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} removed from cart!")
    return redirect('view_cart')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, Product

# views.py in the orders app
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, Product

from django.shortcuts import render
from orders.models import Order
from products.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def farmer_orders(request):
    # Fetch products that belong to the logged-in farmer
    farmer_products = Product.objects.filter(farmer=request.user)

    # Fetch confirmed orders for these products
    orders = Order.objects.filter(products__in=farmer_products, status='CONFIRMED').distinct()

    context = {
        'orders': orders,
    }
    return render(request, 'orders/farmer_order_management.html', context)



# @login_required
# def farmer_orders(request):
#     # Fetch products that belong to the logged-in farmer
#     farmer_products = Product.objects.filter(farmer=request.user)

#     # Fetch orders that include these products
#     orders = Order.objects.filter(products__in=farmer_products).distinct()

#     # If no orders found, check for issues
#     if not orders:
#         print("No orders found for this farmer.")

#     context = {
#         'orders': orders,
#     }
#     return render(request, 'orders/farmer_order_management.html', context)


# @login_required
# def farmer_orders(request):
#     # Fetch products that belong to the logged-in farmer
#     farmer_products = Product.objects.filter(farmer=request.user)
#     # Fetch orders that include these products
#     orders = Order.objects.filter(products__in=farmer_products).distinct()

#     context = {
#         'orders': orders,
#     }
#     return render(request, 'orders/farmer_order_management.html', context)

@login_required
def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.products.first().farmer:
        return HttpResponse("You are not authorized to change the status of this order", status=403)

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            return redirect('order_history')

    #context = {'order': order}
    return render(request, 'orders/change_order_status.html', {'order': order})#context)
