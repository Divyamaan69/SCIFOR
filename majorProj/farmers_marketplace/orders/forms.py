from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter your delivery address...'}))
