from django import forms
from django.contrib.auth import password_validation, authenticate
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from .models import MyUser
from .validators import MyPasswordValidator

import os
import shutil


# This class defines a form for password checking.
class PassowrdCheckForm(forms.Form):
    # This field is for the password input, and is labeled "Password".
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )

    # This field is for confirming the password, and is labeled "Confirm Password".
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
    )

    # This function validates that the two passwords entered match.
    # If they do not match, it raises a validation error.
    def clean_password2(self):
        # Get the cleaned data for password1 and password2.
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # If the passwords do not match, raise a validation error.
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        # Validate the password using Django's built-in password validation.
        password_validation.validate_password(password2)

        # Validate the password using a custom validator (MyPasswordValidator).
        my_validator = MyPasswordValidator()
        try:
            my_validator.validate(password2)
        except ValidationError as e:
            raise forms.ValidationError(e.message, code=e.code)

        # If the validation is successful, return the cleaned password2.
        return password2

# This is a user creation form


class UserCreationForm(forms.Form):

    # email field with required=True attribute to ensure user enters email
    email = forms.EmailField(
        label='Email',
        required=True
    )

    # password1 and password2 fields to take in the user's desired password
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
    )

    # clean_password2 function to ensure password1 and password2 match
    # password validation function to validate the strength of the password entered
    # custom validator to ensure password meets certain requirements
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        password_validation.validate_password(password2)

        my_validator = MyPasswordValidator()

        try:
            my_validator.validate(password2)
        except ValidationError as e:
            raise forms.ValidationError(e.message, code=e.code)

        return password2

    # save function to create a user object and assign the email and password to the object
    # creates a default avatar for the user and saves it in the appropriate directory
    # assigns the avatar path to the user object
    # commits the user object to the database if commit is True
    def save(self, commit=True):
        user = MyUser.objects.create(email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        avatar_dir = os.path.join(
            'media', 'images', 'users', user.email, 'avatar')
        os.makedirs(avatar_dir, exist_ok=True)

        default_avatar_path = os.path.join(
            'media', 'images', 'users', 'default_user', 'avatar', 'user_avatar.png')
        user_avatar_path = os.path.join(avatar_dir, 'default_avatar.png')
        shutil.copyfile(default_avatar_path, user_avatar_path)
        user.avatar = os.path.join(
            'images', 'users', user.email, 'avatar', 'default_avatar.png')
        if commit:
            user.save()
        return user


# Define a form for user registration by email
class RegistrationEmailForm(forms.Form):
    # Define email field with validation rules
    email = forms.EmailField(
        label='Email address',
        validators=[EmailValidator()],
        required=True,
    )

    # Define a function to validate email uniqueness
    def clean_email(self):
        email = self.cleaned_data['email']
        # Check if there's already an account with the same email address
        if MyUser.objects.filter(email=email).exists():
            error_msg = "Email already exists"
            raise forms.ValidationError(error_msg)
        return email


# Define a form for password restoration by email
class PasswordRestoreEmailForm(forms.Form):
    # Define email field with validation rules
    email = forms.EmailField(
        label='Email',
        validators=[EmailValidator()],
        required=True
    )

    # Define a function to validate email existence
    def clean_email(self):
        email = self.cleaned_data['email']
        # Check if there's an account associated with the email address
        if not MyUser.objects.filter(email=email).exists():
            error_msg = "Looks like there isn't an account associated with this email address."
            raise forms.ValidationError(error_msg)
        return email


# Define a form for user sign-in
class SigninForm(forms.Form):
    # Define email field with validation rules
    email = forms.EmailField(
        label='Email',
        validators=[EmailValidator()],
        required=True
    )
    # Define password field with validation rules
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=True
    )

    # Define a function to validate email and password
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Authenticate user by email and password
        user = authenticate(email=email, password=password)
        if user is None:
            error_msg = "Invalid email or password."
            self.add_error('email', error_msg)

        return cleaned_data
