from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    FARMER = 'FARMER'
    BUYER = 'BUYER'
    ROLE_CHOICES = [
        (FARMER, 'Farmer'),
        (BUYER, 'Buyer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.username
