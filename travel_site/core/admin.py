from django.contrib import admin
from django.utils.html import format_html
from .models import Countries

# Register your models here.
@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_photo', 'country_photo_preview')
    list_filter = ('country_name',)
    search_fields = ('country_name',)

    def country_photo_preview(self, obj):
        if obj.country_photo:
            return format_html('<img src="{}" height="50" />'.format(obj.country_photo.url))
        else:
            return "-"
    country_photo_preview.short_description = "Photo Preview"