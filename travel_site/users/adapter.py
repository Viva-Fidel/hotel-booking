from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import authenticate, login
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import MyUser


# class MySocialAccountAdapter(DefaultSocialAccountAdapter):
#     def pre_social_login(self, request, sociallogin):
#         # Check if the email address associated with the social account is already registered
#         if sociallogin.email_addresses:
#             # Get the email address from the social account
#             email = sociallogin.email_addresses[0].email

#             # Check if a user with the same email address already exists
#             if MyUser.objects.filter(email=email).exists():
#                 # Redirect to a custom URL if a user with the same email address already exists
#                 return redirect('/')

#         # Return None to continue with the default behavior
#         return None


# @receiver(pre_social_login)
# def link_to_local_user(sender, request, sociallogin, **kwargs):
#     email = sociallogin.account.extra_data['email']
#     user = authenticate(request, email=email)
#     if user:
#         # Associate the existing local user with the social account
#         sociallogin.connect(request, user)
#     else:
#         # Create a new local user and associate it with the social account
#         data = {
#             'email': email,
#             'username': email.split('@')[0],  # Use the email prefix as the username
#             'password': MyUser.objects.make_random_password(),  # Generate a random password
#         }
#         user = MyUser.objects.create_user(**data)
#         user.is_active = True
#         user.save()
#         sociallogin.connect(request, user)

#     # Log in the user
#     login(request, user)
#     raise ImmediateHttpResponse(redirect('/'))  # Redirect to the home page

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Check if the email address associated with the social account is already registered
        if sociallogin.email_addresses:
            # Get the email address from the social account
            email = sociallogin.email_addresses[0].email

            # Check if a user with the same email address already exists
            if MyUser.objects.filter(email=email).exists():
                # Redirect to a custom URL if a user with the same email address already exists
                return redirect('/')

        # Return None to continue with the default behavior
        return None


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    # Get the email address from the social account
    email = sociallogin.account.extra_data['email']

    try:
        # Try to get the user with the given email
        user = MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        # If the user does not exist, create a new one
        data = {
            'email': email,
            'password': MyUser.objects.make_random_password(),  # Generate a random password
            'first_name': sociallogin.account.extra_data.get('first_name', ''),
            'last_name': sociallogin.account.extra_data.get('last_name', ''),
            'is_active': True,
        }
        user = MyUser.objects.create_user(**data)
        # Create a new local user and associate it with the social account
        
    login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

    # Redirect to the home page
    return redirect('/')
