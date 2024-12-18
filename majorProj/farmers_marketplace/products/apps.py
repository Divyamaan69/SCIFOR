from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

# yourapp/apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'yourapp'

    def ready(self):
        import yourapp.templatetags.custom_filters
