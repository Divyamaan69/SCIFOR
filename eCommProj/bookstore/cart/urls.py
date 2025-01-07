from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
    path('', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),

]
