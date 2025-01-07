from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Home Page - List all books
    path('book/<int:id>/', views.book_detail, name='book_detail'),  # Book Details
    path('cart/', views.cart_view, name='cart_view'),  # Cart Page
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),  # Add to Cart
    path('checkout/', views.checkout, name='checkout'),  # Checkout Page
    path('order-success/', views.order_success, name='order_success'),  # Order Success Page
    path('login/', views.login_view, name='login'),  # Login Page
    path('signup/', views.signup_view, name='signup'),  # Signup Page
    path('logout/', views.logout_view, name='logout'),  # Logout
]
