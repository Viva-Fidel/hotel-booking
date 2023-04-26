from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .forms import UserCreationForm, EmailForm
from django.contrib.auth.models import User
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
                    User.objects.get(email=email)
                except User.DoesNotExist:
                    return JsonResponse({'success': True})
                else:
                    # Email already exists
                    form.add_error('email', 'Email already exists')
            # Return errors if form is invalid
            return JsonResponse({'success': False, 'errors': form.errors})

        # Check if email and passwords are provided
        elif email and password1 and password2:
            form = UserCreationForm({
                'username': email,
                'email': email,
                'password1': password1,
                'password2': password2,
            })

            print(form.errors)
            if form.is_valid():
                user = form.save()
                # Log in the user
                login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                return redirect('/')
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
           
    # Return the registration form
    form = EmailForm()
    return render(request, 'accounts/authentification.html', {'form': form})
