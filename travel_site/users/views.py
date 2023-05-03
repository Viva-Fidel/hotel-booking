from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .forms import UserCreationForm, RegistrationEmailForm, SigninForm, PasswordRestoreEmailForm, PassowrdCheckForm
from .models import MyUser
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse

def set_new_password(request, uidb64, token):
    form = PassowrdCheckForm()
    context = {'form': form, 'title': 'Create password',
               'button': 'Create new password'}
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = MyUser.objects.get(email=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    
    if user and PasswordResetTokenGenerator().check_token(user, token):
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            form = PassowrdCheckForm({
            'password1': password1,
            'password2': password2,
        })
            if form.is_valid():
                user.set_password(password1)
                user.save()
                login(request, user,
                  backend='allauth.account.auth_backends.AuthenticationBackend')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, "users/password_reset_confirm.html", context)


def password_reset_done(request):
    email = request.session.get('reset_email', '')
    context = {'title': 'Check your Inbox',
               'button': 'Back to Sign in', 'email': email}
    return render(request, 'users/authentification.html', context)


def password_reset(request):
    form = PasswordRestoreEmailForm()
    context = {'form': form, 'title': 'Forgot your password?',
               'button': 'Send Reset Link'}
    if request.method == 'POST':
        email = request.POST.get('email')
        form = PasswordRestoreEmailForm({'email': email})
        if form.is_valid():
            user = MyUser.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
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

            request.session['reset_email'] = email

            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': form.errors})
    return render(request, 'users/authentification.html', context)


def signin(request):
    form = SigninForm()
    context = {'form': form, 'title': 'Sign In',
               'button': 'Continue with Email'}
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        keep_signed_in = bool(request.POST.get('keep_signed_in'))

        form = SigninForm({'email': email, "password": password})
        if form.is_valid():
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if keep_signed_in:
                    request.session.set_expiry(30 * 24 * 60 * 60)
                else:
                    request.session.set_expiry(24 * 60 * 60)

                login(request, user)
                return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return render(request, 'users/authentification.html', context)


def registration(request):

    form = RegistrationEmailForm()
    context = {'form': form, 'register_title': 'Register',
               'create_password_title': 'Create Password', 'button': 'Continue with Email'}

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
                user = form.save()
                login(
                    request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'users/authentification.html', context)
