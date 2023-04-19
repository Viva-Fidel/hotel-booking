from django.urls import path
from . import views
from blogs.views import blog_detail


from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_address),
    path('search/hotels/', views.search_hotels, name='search_hotels'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),

]

urlpatterns += staticfiles_urlpatterns()