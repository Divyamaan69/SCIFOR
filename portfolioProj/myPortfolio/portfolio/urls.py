from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tech/<int:pk>/', views.tech_detail, name='tech_detail'),
    path('writing/<int:pk>/', views.writing_detail, name='writing_detail'),
]
