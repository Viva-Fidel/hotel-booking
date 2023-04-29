from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registration, name='registration'),
    path('register/', include('allauth.urls')),
    path('signin/', views.signin, name='signin'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/',  views.set_new_password, name='password_reset_confirm'),
]