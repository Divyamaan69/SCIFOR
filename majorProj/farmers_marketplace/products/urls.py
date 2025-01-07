from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('buyer/home/', views.buyer_home, name='buyer_home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('farmer/add/', views.add_product, name='add_product'),
    path('farmer/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('farmer/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/message/', views.send_message, name='send_message'),
    path('farmer/inbox/', views.farmer_inbox, name='farmer_inbox'),
    path('farmer/messages/respond/<int:message_id>/', views.respond_to_message, name='respond_to_message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)