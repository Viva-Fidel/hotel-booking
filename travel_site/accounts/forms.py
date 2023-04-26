from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from .models import MyUser



class UserCreationForm(UserCreationForm):

    
    email = forms.EmailField(
        label='Email',
        validators=[EmailValidator()],
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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            error_msg = "Email already exists"
            self.add_error('email', error_msg)
        return email
    
    
    class Meta:
        model = User
        fields = ('email',)



class EmailForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        validators=[EmailValidator()],
        required=True
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            error_msg = "Email already exists"
            self.add_error('email', error_msg)
        return email



