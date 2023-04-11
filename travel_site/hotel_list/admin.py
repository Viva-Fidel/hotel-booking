from django.contrib import admin
from .models import Hotel_list

# Register your models here.


@admin.register(Hotel_list)
class Hotel_listAdmin(admin.ModelAdmin):
    list_display = ('hotel_name', 'hotel_country', 'hotel_city', 'hotel_street',
                    'hotel_photo', 'time_create', 'is_published')
    list_filter = ('is_published', 'hotel_country', 'hotel_city')
    search_fields = ('hotel_name', 'hotel_country', 'hotel_city')
