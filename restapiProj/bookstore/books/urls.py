from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, test_auth

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-auth/', test_auth),
]