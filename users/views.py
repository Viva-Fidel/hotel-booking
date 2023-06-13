from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import UserCreationForm, RegistrationEmailForm, SigninForm, PasswordRestoreEmailForm, PassowrdCheckForm
from .models import MyUser


def set_new_password(request, uidb64, token):
    # Create a form object to display on the page
    form = PassowrdCheckForm()
    # Define the context dictionary with the appropriate information
    context = {'form': form, 'title': 'Create password',
               'button': 'Create new password'}
    try:
        # Attempt to decode the uid from the URL
        uid = urlsafe_base64_decode(uidb64).decode()
        # Look up the user with the decoded uid
        user = MyUser.objects.get(email=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        # If an error occurs, set the user to None
        user = None
    
    print(token)
    
    # If a valid user is found and the token is valid
    if user and PasswordResetTokenGenerator().check_token(user, token):
        if request.method == "POST":
            # Retrieve the password fields from the form
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Create a form object with the provided password fields
            form = PassowrdCheckForm(
                {'password1': password1, 'password2': password2})
            
            # If the form is valid
            if form.is_valid():
                # Set the user's password to the provided password
                user.set_password(password1)
                user.save()
                # Log the user in
                login(
                    request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                return JsonResponse({'success': True})
            else:
                # If the form is not valid, return the errors as JSON
                return JsonResponse({'success': False, 'errors': form.errors})

    # Render the template with the appropriate context
    return render(request, "users/password_reset_confirm.html", context)


def password_reset_done(request):

    # View for displaying a success message after a password reset email has been sent to the user.

    email = request.session.get('reset_email', '')
    context = {'title': 'Check your Inbox',
               'button': 'Back to Sign in', 'email': email}
    return render(request, 'users/authentification.html', context)


def password_reset(request):
    # Create a new instance of PasswordRestoreEmailForm
    form = PasswordRestoreEmailForm()
    # Create a context dictionary containing the form, title, and button label
    context = {'form': form, 'title': 'Forgot your password?',
               'button': 'Send Reset Link'}
    if request.method == 'POST':
        # Get the email from the POST request
        email = request.POST.get('email')
        # Create a new instance of PasswordRestoreEmailForm with the email field pre-filled
        form = PasswordRestoreEmailForm({'email': email})
        if form.is_valid():
            # If the form is valid, get the user associated with the email
            user = MyUser.objects.get(email=email)
            # Generate a password reset token for the user
            token = PasswordResetTokenGenerator().make_token(user)
            # Encode the email and token as base64 strings
            uidb64 = urlsafe_base64_encode(force_bytes(email))
            # Generate the password reset URL
            restore_url = reverse('password_reset_confirm', kwargs={
                                  'uidb64': uidb64, 'token': token})
            restore_url = request.build_absolute_uri(restore_url)
            
            subject = 'Password reset'
            template_name = 'users/password_reset_email.html'
            context = {'restore_url': restore_url}
            from_email = 'alexi.artamonov@yandex.ru'
            recipient_list = [email]
            html_message = render_to_string(template_name, context)

            # Send a password reset email to the user
            send_mail(
                subject=subject,
                message='',
                html_message=html_message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )

            # Store the email address in the session
            request.session['reset_email'] = email

            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': form.errors})
    # Render the password reset template with the context dictionary
    return render(request, 'users/authentification.html', context)


def signin(request):
    # create an instance of the SigninForm
    form = SigninForm()

    # define a dictionary context with the form instance, title, and button text
    context = {'form': form, 'title': 'Sign In',
               'button': 'Continue with Email'}

    if request.method == 'POST':
        # retrieve the user's email, password, and keep_signed_in preference from the POST request
        email = request.POST.get('email')
        password = request.POST.get('password')
        keep_signed_in = bool(request.POST.get('keep_signed_in'))

        # create an instance of the SigninForm with the email and password data
        form = SigninForm({'email': email, "password": password})

        # check if the form data is valid
        if form.is_valid():
            # authenticate the user with the given email and password
            user = authenticate(request, email=email, password=password)

            # if the user is authenticated successfully
            if user is not None:
                # set the session timeout based on the keep_signed_in preference
                if keep_signed_in:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                else:
                    request.session.set_expiry(24 * 60 * 60)  # 1 day

                # log the user in and return a success response
                login(request, user)
                return JsonResponse({'success': True})

        # if the form data is not valid, return an error response with the form errors
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # if the request method is not POST, render the authentication template with the context dictionary
        return render(request, 'users/authentification.html', context)


def registration(request):

    # Instantiate the RegistrationEmailForm and set up the context dictionary
    form = RegistrationEmailForm()
    context = {'form': form, 'register_title': 'Register',
               'create_password_title': 'Create Password', 'button': 'Continue with Email'}

    # If the request method is POST, handle form submission
    if request.method == 'POST':

        # Get email, password1 and password2 from the POST request
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # If email is present and password1 and password2 are not, validate the email field
        if email and not password1 and not password2:
            form = RegistrationEmailForm({'email': email})
            if form.is_valid():
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors})

        # If email and password1 and password2 are present, validate the UserCreationForm
        elif email and password1 and password2:
            form = UserCreationForm({
                'email': email,
                'password1': password1,
                'password2': password2,
            })

            # If the form is valid, create the user, log them in and return a success message
            if form.is_valid():
                user = form.save()
                login(
                    request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                return JsonResponse({'success': True})

            # If the form is not valid, return an error message
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

    # Render the authentication template with the context dictionary
    return render(request, 'users/authentification.html', context)
