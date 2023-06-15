from django.urls import path, include
from . import views


from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('book', views.book, name='book'),

]

urlpatterns += staticfiles_urlpatterns()