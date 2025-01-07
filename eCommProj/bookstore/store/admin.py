from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, Cart, Order, OrderItem

admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
