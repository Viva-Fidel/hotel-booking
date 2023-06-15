from django.urls import path, include
from . import views
from .views import hotel_detail, get_api_data


from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('hotel/<slug:slug>/', hotel_detail, name='hotel_detail'),
    path('get_api_data', get_api_data, name='get_api_data'),

]

urlpatterns += staticfiles_urlpatterns()