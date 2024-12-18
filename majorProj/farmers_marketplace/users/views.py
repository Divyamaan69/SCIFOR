from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save#(commit=False)
#             role = request.POST.get('role')
#             user.role = role
#             user.save()
#             login(request, user)
#             if role == 'farmer':
#                 return redirect('farmer_dashboard')  # Farmer's dashboard
#             else:
#                 return redirect('buyer_home')   # Buyer's dashboard
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'users/register.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')  # Redirect to a home page or dashboard
#     else:
#         form = AuthenticationForm()
#     return render(request, 'users/login.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            if user.role == 'FARMER':  # Check user role
                return redirect('farmer_dashboard')  # Redirect to farmer dashboard
            elif user.role == 'BUYER':  # Check user role
                return redirect('buyer_home')  # Redirect to buyer home
        else:
            # Add an error message for invalid credentials
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, 'users/login.html')  # Render login page for GET or invalid POST

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             if user.role == 'FARMER':
#                 return redirect('farmer_dashboard')
#             else:
#                 return redirect('buyer_home')
#     return render(request, 'users/login.html')

def farmer_dashboard(request):
    return render(request, 'products/farmer_dashboard.html')

def buyer_home(request):
    return render(request, 'products/buyer_home.html')

# @login_required
# def admin_home(request):
#     # Check the user role and redirect accordingly
#     if request.user.role == 'farmer':
#         return redirect('products/farmer_dashboard.html')
#     elif request.user.role == 'buyer':
#         return redirect('products/buyer_home.html')
#     return render(request, 'users/admin_home.html')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def admin_home(request):
    context = {
        'is_farmer': request.user.role == 'FARMER',
        'is_buyer': request.user.role == 'BUYER',
    }
    return render(request, 'users/admin_home.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            if user.role == 'FARMER':  # Redirect based on user role
                return redirect('farmer_dashboard')
            elif user.role == 'BUYER':
                return redirect('buyer_home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})
