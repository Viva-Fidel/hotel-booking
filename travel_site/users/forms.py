from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import MyUser
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from .validators import MyPasswordValidator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm



class PassowrdCheckForm(forms.Form):
    password1 = forms.CharField(
          label='Password',
          widget=forms.PasswordInput,
      )

    password2 = forms.CharField(
          label='Confirm Password',
          widget=forms.PasswordInput,
      )
    
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

class UserCreationForm(forms.Form):

    
    email = forms.EmailField(
        label='Email',
        required=True
    )
    password1 = forms.CharField(
          label='Password',
          widget=forms.PasswordInput,
      )

    password2 = forms.CharField(
          label='Confirm Password',
          widget=forms.PasswordInput,
      )
    
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


class RegistrationEmailForm(forms.Form):
    email = forms.EmailField(
        label='Email address',
        validators=[EmailValidator()],
        required=True,
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if MyUser.objects.filter(email=email).exists():
            error_msg = "Email already exists"
            raise forms.ValidationError(error_msg)
        return email
    
class PasswordRestoreEmailForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        validators=[EmailValidator()],
        required=True
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not MyUser.objects.filter(email=email).exists():
            error_msg = "Looks like there isn't an account associated with this email address."
            raise forms.ValidationError(error_msg)
        return email
    
class SigninForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        validators=[EmailValidator()],
        required=True
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            error_msg = "Invalid email or password."
            self.add_error('email', error_msg)

        return cleaned_data



