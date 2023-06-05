from django.urls import path, include
from . import views
from .views import hotels


from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('hotel', views.hotels, name='hotels'),

]

urlpatterns += staticfiles_urlpatterns()