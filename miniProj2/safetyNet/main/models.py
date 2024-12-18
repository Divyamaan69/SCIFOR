from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    city = models.CharField(max_length=100)
    govt_id = models.ImageField(upload_to="photos/", blank=True, null=True, default='')

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()
