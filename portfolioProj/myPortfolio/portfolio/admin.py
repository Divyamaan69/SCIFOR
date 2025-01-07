from django.contrib import admin

# Register your models here.
from .models import TechExample, WritingExample

admin.site.register(TechExample)
admin.site.register(WritingExample)
