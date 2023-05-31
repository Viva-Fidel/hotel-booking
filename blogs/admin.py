from django.contrib import admin
from django.utils.html import format_html
from .models import Blogs


# Register your models here.


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'blog_photo', 'blog_photo_preview',
                    'time_create', 'is_published', 'slug',)
    list_filter = ('is_published',)
    search_fields = ('blog_title',)
    exclude = ('slug',)

    # Define a method that returns a preview of the county photo in the admin UI
    def blog_photo_preview(self, obj):
        # If a photo is present, display a thumbnail
        if obj.blog_photo:
            return format_html('<img src="{}" height="50" />'.format(obj.blog_photo.url))
        # If no photo is present, display a placeholder
        else:
            return "-"
    # Set a user-friendly name for the county photo preview column
    blog_photo_preview.short_description = "Photo Preview"