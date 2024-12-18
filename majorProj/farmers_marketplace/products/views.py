from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Message

# Create your views here.
@login_required
def farmer_dashboard(request):
    products = Product.objects.filter(farmer=request.user)
    return render(request, 'products/farmer_dashboard.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            return redirect('farmer_dashboard')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('farmer_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('farmer_dashboard')
    return render(request, 'products/delete_product.html', {'product': product})

from django.db.models import Q

@login_required
def buyer_home(request):
    query = request.GET.get('q', '')  # Search query
    category_filter = request.GET.get('category', '')  # Category filter
    products = Product.objects.all()

    # Apply search and filters to the products
    if query:
        products = products.filter(name__icontains=query)
    if category_filter:
        products = products.filter(category=category_filter)

    paginator = Paginator(products, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all messages where the current user (buyer) is the recipient
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')

    # For each message, get its responses (if any)
    for message in messages:
        # Use .all() on the related set to fetch all responses
        message.responses_list = message.responses.all()

    categories = Product.objects.values_list('category', flat=True).distinct()

    return render(request, 'products/buyer_home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'category_filter': category_filter,
        'messages': messages,  # Pass the messages to the template
        'products': products,  # Ensure products are passed to the template
    })



# @login_required
# def buyer_home(request):
#     query = request.GET.get('q', '')  # Search query
#     category_filter = request.GET.get('category', '')  # Category filter
#     products = Product.objects.all()

#     # Apply search and filters to the products
#     if query:
#         products = products.filter(name__icontains=query)
#     if category_filter:
#         products = products.filter(category=category_filter)

#     paginator = Paginator(products, 6)  # 6 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Get all messages where the current user (buyer) is the recipient
#     messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')

#     # For each message, get its responses (if any)
#     for message in messages:
#         message.responses = Message.objects.filter(parent_message=message)

#     categories = Product.objects.values_list('category', flat=True).distinct()

#     return render(request, 'products/buyer_home.html', {
#         'page_obj': page_obj,
#         'categories': categories,
#         'query': query,
#         'category_filter': category_filter,
#         'messages': messages,  # Pass the messages to the template
#     })


# def buyer_home(request):
#     query = request.GET.get('q', '')  # Search query
#     category_filter = request.GET.get('category', '')
#     products = Product.objects.all()

#     # Apply search and filters
#     if query:
#         products = products.filter(name__icontains=query)
#     if category_filter:
#         products = products.filter(category=category_filter)

#     paginator = Paginator(products, 6)  # 6 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     categories = Product.objects.values_list('category', flat=True).distinct()
#     return render(request, 'products/buyer_home.html', {
#         #'products': products,
#         'page_obj': page_obj,
#         'categories': categories,
#         'query': query,
#         'category_filter': category_filter,
#     })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def send_message(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    farmer = product.farmer

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = farmer
            message.product = product
            message.save()
            messages.success(request, 'Your message has been sent!')
            return redirect('product_detail', pk=product_id)
    else:
        form = MessageForm()

    return render(request, 'products/send_message.html', {'form': form, 'product': product})

@login_required
def farmer_inbox(request):
    # Get all messages where the current user (farmer) is the recipient
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'products/farmer_inbox.html', {'messages': messages})

@login_required
def respond_to_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)

    # Ensure that the logged-in user is the recipient (farmer)
    if request.user != message.recipient:
        return redirect('farmer_inbox')  # Redirect if the user is not the intended recipient

    if request.method == 'POST':
        response = request.POST.get('response')
        if response:
            # Create a reply message from the farmer to the buyer
            reply_message = Message.objects.create(
                sender=request.user,  # Farmer is sending the reply
                recipient=message.sender,  # The buyer is the recipient
                product=message.product,  # Same product being discussed
                message=response,
                parent_message=message  # Link the response to the original message
            )
            message.save()  # Optionally mark the original message as read
            return redirect('farmer_inbox')  # Redirect back to the inbox after reply

    return render(request, 'products/respond_to_message.html', {'message': message})
