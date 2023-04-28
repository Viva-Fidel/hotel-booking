from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .forms import UserCreationForm, RegistrationEmailForm, SigninForm, PasswordRestoreEmailForm
from .models import MyUser
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from .tokens import email_token_generator



def password_reset_done(request):
    return render(request, 'users/authentification.html')


def password_reset(request):
    form = PasswordRestoreEmailForm()
    context = {'form': form, 'title': 'Forgot your password?', }
    if request.method == 'POST':
        email = request.POST.get('email')
        form = PasswordRestoreEmailForm({'email': email})
        if form.is_valid():
            token = email_token_generator.make_token(email)
            uidb64 = urlsafe_base64_encode(force_bytes(email))
            restore_url = reverse('password_reset_confirm', kwargs={
                                  'uidb64': uidb64, 'token': token})
            restore_url = request.build_absolute_uri(restore_url)

            # Send restore email
            num_sent = send_mail(
                    'Password reset',
                    f'Please click on the following link to reset your password: {restore_url}',
                    'alexi.artamonov@yandex.ru',
                    [email],
                    fail_silently=False,
                )
            print(f'{num_sent} email(s) sent successfully')
            

            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': form.errors})
    return render(request, 'users/authentification.html', context)




def signin(request):
    form = SigninForm()
    context = {'form': form, 'title': 'Sign In', }
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        keep_signed_in = bool(request.POST.get('keep_signed_in'))

        form = SigninForm({'email': email, "password": password})
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if keep_signed_in:
                    # Set session expiry to 30 days
                    request.session.set_expiry(30 * 24 * 60 * 60)
                else:
                    # Set session expiry to 1 day
                    request.session.set_expiry(24 * 60 * 60)

                login(request, user)
                return JsonResponse({'success': True})
        # If the form is invalid, return a JSON response with the error messages
        # return render(request, 'users/authentification.html', {'form': form, 'errors': form.errors})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return render(request, 'users/authentification.html', context)


def registration(request):

    form = RegistrationEmailForm()
    context = {'form': form, 'register_title': 'Register', 'create_password_title': 'Create Password', 'button': 'Continue with Email'}
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if email and not password1 and not password2:
            form = RegistrationEmailForm({'email': email})
            if form.is_valid():
                    return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors})

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
                login(
                    request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'users/authentification.html', context)
