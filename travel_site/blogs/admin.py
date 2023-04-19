from django.contrib import admin
from .models import Blogs


# Register your models here.
@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'blog_photo', 'time_create', 'is_published', 'slug',)
    list_filter = ('is_published',)
    search_fields = ('blog_title',)
    exclude = ('slug',)
    