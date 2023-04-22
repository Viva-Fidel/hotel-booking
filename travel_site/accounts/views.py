from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import MyUserCreationForm, SignInForm
from django.contrib import messages
# Create your views here.

def registration(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = MyUserCreationForm()
    return render(request, 'accounts/authentification.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = SignInForm()
    return render(request, 'accounts/authentification.html', {'form': form})