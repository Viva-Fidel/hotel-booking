from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .forms import UserCreationForm, EmailForm
from .models import MyUser
from django.contrib import messages


def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if only email is provided
        if email and not password1 and not password2:
            form = EmailForm({'email': email})
            if form.is_valid():
                email = form.cleaned_data['email']
                # Check if email already exists
                try:
                    MyUser.objects.get(email=email)
                except MyUser.DoesNotExist:
                    return JsonResponse({'success': True})
                else:
                    # Email already exists
                    form.add_error('email', 'Email already exists')
            # Return errors if form is invalid
            return JsonResponse({'success': False, 'errors': form.errors})

        # Check if email and passwords are provided
        elif email and password1 and password2:
            form = UserCreationForm({
                'email': email,
                'password1': password1,
                'password2': password2,
            })


            if form.is_valid():
                user = MyUser.objects.create(email=email, password=password1)
                user.set_password(password1)
                user.save()
                login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
           
    # Return the registration form
    form = EmailForm()
    return render(request, 'users/authentification.html', {'form': form})
