from django import forms 
from .models import pgRoom, complaintForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class pgForm(forms.ModelForm):
    class Meta:
        model = pgRoom
        fields = ['user', 'location', 'photo', 'room', 'price', 'food']

class pgComplaint(forms.ModelForm):
    class Meta:
         model = complaintForm
         email = forms.EmailField(label="email")
         complaint = forms.CharField(widget=forms.Textarea, label="complaint")
         fields = ['email', 'complaint']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')