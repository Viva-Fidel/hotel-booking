from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.registration, name='registration'),
    path('register/', include('allauth.urls')),
    path('signin/', views.signin, name='signin'),
]