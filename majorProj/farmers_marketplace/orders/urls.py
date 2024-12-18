from django.urls import path
from . import views

app_name = 'orders'  # Add the app_name here

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/place_order/', views.place_order, name='place_order'),
    path('farmer/orders/', views.farmer_orders, name='farmer_orders'),
    path('order/change-status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    #path('farmer/order/<int:order_id>/change_status/', views.change_order_status, name='change_order_status'),
]
