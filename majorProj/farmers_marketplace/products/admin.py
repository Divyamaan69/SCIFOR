from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Message

admin.site.register(Product)
admin.site.register(Message)