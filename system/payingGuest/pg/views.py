from django.shortcuts import render, redirect
from .models import pgRoom, complaintForm
from .forms import pgForm, pgComplaint, UserRegistrationForm
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden

# Create your views here.

def index(request):
    return render(request, 'index.html')

def pg_list(request):
    PGs = pgRoom.objects.all().order_by('price')
    return render(request, 'pg_list.html', {'PGs': PGs})

@login_required
def pg_create(request):
    if pgRoom.objects.filter(user=request.user).exists():
        return render(request,'pg_list.html', {'already_created': True})

    if request.method == "POST":
        form = pgForm(request.POST, request.FILES)
        if form.is_valid():
            pg = form.save(commit=False)
            pg.user = request.user
            pg.save()
            return redirect('pg_list')
    else:
        form = pgForm()
    return render(request, 'pg_form.html', {'form': form})

@login_required
def pg_edit(request, pg_id):
    pg = get_object_or_404(pgRoom, pk=pg_id, user = request.user)
    if request.method == 'POST':
        form = pgForm(request.POST, request.FILES, instance = pg)
        if form.is_valid():
            pg = form.save(commit = False)
            pg.user = request.user
            pg.save()
            return redirect('pg_list')
    else:
        form = pgForm(instance = pg)
    return render(request, 'pg_form.html', {'form': form})

@login_required
def pg_delete(request, pg_id):
    pg = get_object_or_404(pgRoom, pk=pg_id, user = request.user)
    if request.method == 'POST':
        pg.delete()
        return redirect('pg_list')
    return render(request, 'pg_confirm_delete.html', {'pg': pg})

# Sending a complaint via Email
def send_complaint(request):
    if request.method == "POST":
        form = pgComplaint(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            complaint = form.cleaned_data['complaint']
            # Send the email
            send_mail(
                'Complaint from Paying Guest Management System',  # Subject
                complaint,                    # Message body
                settings.DEFAULT_FROM_EMAIL,  # From email
                [email],            # To email list
                fail_silently=False,
            )
            return redirect('success_view')  # Redirect to a success page or thank you message
    else:
        form = pgComplaint()

    return render(request, 'pg_complaint.html', {'form': form})

# views.py
def success_view(request):
    return render(request, 'success.html')

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('pg_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
