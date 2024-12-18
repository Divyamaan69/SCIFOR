# Create your views here.
from django.shortcuts import render, redirect
from .forms import UserProfileForm, ContactForm, UserRegistrationForm, PanicForm
from .models import Contact, Profile
from django.core.mail import send_mail
from django.utils.timezone import now
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # user = 
            form.save()
            # user.set_password(form.cleaned_data['password'])
            # user.save()
            # login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('home')

def home(request):
    pfs = Profile.objects.all()
    return render(request, 'main/home.html', {'pfs': pfs})


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)  # Don't save the contact yet
            contact.user = request.user  # Set the user field to the logged-in user
            contact.save()  # Now save the contact with the user field set
            return redirect('contacts')  # Redirect after successful form submission
    else:
        form = ContactForm()

    # Get all contacts for the logged-in user, assuming you want to display only the user's contacts
    contacts = Contact.objects.filter(user=request.user)
    #contacts = Contact.objects.all()
    return render(request, 'main/contacts.html', {'form': form, 'contacts': contacts})

def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return redirect('contacts')

@login_required
def profile(request):
    if Profile.objects.filter(user=request.user).exists():
        return render(request,'main/home.html', {'already_created': True})

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            pf = form.save(commit=False)
            pf.user = request.user
            pf.save()
            return redirect('home')
    else:
        form = UserProfileForm()
    return render(request, 'main/profile.html', {'form': form})


from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.conf import settings
from datetime import datetime
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from datetime import datetime
from .forms import PanicForm
from .models import Contact
from django.conf import settings

def panic(request):
    if request.method == "POST":
        form = PanicForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            current_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')

            # Pre-written message
            message = f"Help me, I am in danger.\nCurrent city: {city}\nTime: {current_time}"

            # Email recipients
            police_email = "divyamaan14@gmail.com"  # Replace with the actual email
            contacts = Contact.objects.filter(user=request.user)
            contact_emails = [contact.email for contact in contacts]

            # Combine recipients
            recipients = [police_email] + contact_emails

            # Send the email directly without preview
            try:
                send_mail(
                    subject="Emergency: Need Help",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipients,
                    fail_silently=False,
                )
                return redirect('home')  # Redirect after sending the email
            except Exception as e:
                print(f"Error sending email: {e}")
                return render(request, 'main/panic.html', {
                    'error': 'An error occurred while sending the email.',
                    'form': form,
                })
    else:
        form = PanicForm()

    return render(request, 'main/panic.html', {'form': form})
