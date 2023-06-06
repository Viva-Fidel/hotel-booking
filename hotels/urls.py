from django.urls import path, include
from . import views
from .views import hotel_detail


from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('hotel/<slug:slug>/', hotel_detail, name='hotel_detail'),

]

urlpatterns += staticfiles_urlpatterns()