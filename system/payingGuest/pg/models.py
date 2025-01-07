from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class pgRoom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.TextField(max_length=500)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True, default='default.jpg')
    room = models.TextField(max_length=50)
    price = models.IntegerField()
    food = models.TextField(max_length=50)
    complaint = models.TextField(max_length=5000)

    def __str__(self):
        return f'{self.user.username} - {self.location} - {self.room}'

class complaintForm(models.Model):
    email = models.CharField(max_length=500)
    complaint = models.TextField(max_length=5000)

    def __str__(self):
        return f'{self.email} - {self.complaint}'