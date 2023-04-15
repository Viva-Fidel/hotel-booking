from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_address),
    path('search/hotels/', views.search_hotels, name='search_hotels'),
]

urlpatterns += staticfiles_urlpatterns()