from django.urls import path, include
from . import views
from blogs.views import blog_detail


from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_address),
    path('search/hotels/', views.search_hotels, name='search_hotels'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('update-search-results/', views.update_search_results, name='update_search_results'),

]

urlpatterns += staticfiles_urlpatterns()