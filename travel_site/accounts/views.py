from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .forms import UserCreationForm, EmailForm
from django.contrib.auth.models import User
from django.contrib import messages


# from formtools.wizard.views import SessionWizardView
# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from django.contrib.auth import authenticate, login
# from django.contrib import messages

# from .forms import EmailForm, PasswordForm
# from django.contrib.auth.models import User

# class RegistrationWizard(SessionWizardView):
#     template_name = 'accounts/authentification.html'
#     form_list = [EmailForm, PasswordForm]


#     # def get_form_initial(self, step):

#     #     # set initial values for the forms
#     #     initial = self.initial_dict.get(step, {})
#     #     return initial

#     def done(self, form_list, **kwargs):
#         # handle form submission
#         email = form_list[0].cleaned_data['email']
#         password = form_list[1].cleaned_data['password1']
#         # do something with the form data, e.g. create a new user
#         action = self.request.POST.get('action')
#         if action == 'create':
#             return render(self.request, 'registration_done.html', {'email': email, 'password': password})
#         else:
#             return render(self.request, 'registration_not_done.html', {'email': email, 'password': password})



# alexis.artamonov@gmail.com

# Create your views here.

# def registration(request):
#     print(request.POST)
    
#     if request.method == 'POST':
#         email = request.POST.get('the_post')
#         form = EmailForm()
#         print(form.cleaned_data)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             print(email)
#             pass
#     else:
#         form = EmailForm()
#     return render(request, 'accounts/authentification.html', {'form': form})


def registration(request):

    print(request.POST)

    if request.method == 'POST':
        email = request.POST.get('the_post')
        form = EmailForm({'email': email})
        print(form.is_valid())
        if form.is_valid():
            email = form.cleaned_data['email']
            # Do something with the email (e.g. create a new user)
            pass
        else:
            # If form is not valid, print out the errors
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EmailForm()
    return render(request, 'accounts/authentification.html', {'form': form})


# def registration(request):
#     if request.method == 'POST':
#         if 'email' in request.POST:
#             email = request.POST['email']
#             request.session['email'] = email
#         elif 'password' in request.POST:
#             password_form = PasswordForm(request.POST)
#             if password_form.is_valid():
#                 password1 = password_form.cleaned_data.get('password')
#                 password2 = password_form.cleaned_data.get('confirm_password')

#             if password1 != password2:
#                  messages.error(request, 'Passwords do not match.')
#                  return redirect('/register')

#             email = request.session.get('email')
#             user = User.objects.create_user(username=email, email=email, password=password1)
#             user.save()
 
#             login(request, user)
#             messages.success(request, 'You are now registered and logged in.')

#             request.session.flush()
#             return redirect('/')
#     else:
#         email_form = EmailForm()
#         password_form = PasswordForm()
#         return render(request, 'accounts/authentification.html', {'email_form': email_form, 'password_form': password_form})

    
    # # First Step: Get Email
    # if 'email' in request.POST:
    #     email = request.POST.get('email')
    #     request.session['email'] = email
    #     # No return statement needed here.

    # # Second Step: Get Passwords
    # elif request.method == 'POST' and 'password_form' in request.POST:
    #     password_form = PasswordForm(request.POST)
    #     # Validate passwords
    #     if password_form.is_valid():
    #         password1 = password_form.cleaned_data.get('password')
    #         password2 = password_form.cleaned_data.get('confirm_password')
    #         # Validate passwords
    #         if password1 != password2:
    #             messages.error(request, 'Passwords do not match.')
    #             return redirect('/register')
    #         # Create User
    #         email = request.session.get('email')
    #         user = User.objects.create_user(username=email, email=email, password=password1)
    #         user.save()
    #         # Log user in and redirect to home page
    #         login(request, user)
    #         messages.success(request, 'You are now registered and logged in.')
    #         # Clear session
    #         request.session.flush()
    #         return redirect('/')
    #     else:
    #         # Render the same registration template with errors
    #         return render(request, 'accounts/authentification.html', {'password_form': password_form})

    # # Initial Page Load
    # else:
    #     email_form = EmailForm()
    #     password_form = PasswordForm()
    #     return render(request, 'accounts/authentification.html', {'email_form': email_form, 'password_form': password_form})





# def signin(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Invalid email or password.')
#     else:
#         form = SignInForm()
#     return render(request, 'accounts/authentification.html',)