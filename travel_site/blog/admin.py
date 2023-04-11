from django.contrib import admin
from .models import Blog_post

# Register your models here.

# Register your models here.
@admin.register(Blog_post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'blog_photo', 'time_create', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('blog_photo',)