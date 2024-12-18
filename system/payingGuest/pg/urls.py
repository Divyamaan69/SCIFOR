from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.pg_list, name = 'pg_list'),

    path('create/', views.pg_create, name = 'pg_create'),

    path('<int:pg_id>/edit/', views.pg_edit, name = 'pg_edit'),

    path('<int:pg_id>/delete/', views.pg_delete, name = 'pg_delete'),

    path('complaint/', views.send_complaint, name='send_complaint'),

    path('success/', views.success_view, name='success_view'),

    path('register/', views.registration, name='registration'),
]

