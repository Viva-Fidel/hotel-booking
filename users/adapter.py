from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import login
from allauth.account.utils import perform_login
from django.dispatch import receiver
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from allauth.exceptions import ImmediateHttpResponse
from django.conf import settings
from .models import MyUser

import requests


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Check if the email address associated with the social account is already registered
        if sociallogin.email_addresses:
            # Get the email address from the social account
            email = sociallogin.email_addresses[0].email

            # Check if a user with the same email address already exists
            if MyUser.objects.filter(email=email).exists():
                # Redirect to a custom URL if a user with the same email address already exists
                return redirect('home')

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
        avatar_url = sociallogin.account.extra_data.get('picture', '')
        response = requests.get(avatar_url)
        if response.status_code == 200:
            file_name = f'user_avatar.jpg'
            file_path = f'images/users/{email}/avatar/{file_name}'
            file_content = ContentFile(response.content)
            default_storage.save(file_path, file_content)
        else:
            default_user_image_path = 'images/users/default_user/avatar/user_avatar.png'
            with open(default_user_image_path, 'rb') as f:
                file_content = ContentFile(f.read())
            file_path = f'images/users/{email}/avatar/default_avatar.png'
            default_storage.save(file_path, file_content)

        # If the user does not exist, create a new one
        data = {
            'email': email,
            'password': MyUser.objects.make_random_password(),  # Generate a random password
            'first_name': sociallogin.account.extra_data.get('first_name', ''),
            'last_name': sociallogin.account.extra_data.get('last_name', ''),
            'avatar': file_path,
            'is_active': True,
        }
        user = MyUser.objects.create_user(**data)
    
    if user:
        perform_login(request, user, email_verification='optional')
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL.format(id=request.user.id)))

    