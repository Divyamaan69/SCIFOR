from django.urls import path
from .views import register_view, login_view
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('buyer/home/', views.buyer_home, name='buyer_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
]
