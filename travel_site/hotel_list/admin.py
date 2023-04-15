from django.contrib import admin
from .models import Hotel_list
from django import forms
from core.models import Countries

# Register your models here.
class HotelForm(forms.ModelForm):
    hotel_country = forms.ModelChoiceField(queryset=Countries.objects.all())

    class Meta:
        model = Hotel_list
        fields = '__all__'

@admin.register(Hotel_list)
class Hotel_listAdmin(admin.ModelAdmin):
    form = HotelForm
    list_display = ('hotel_name', 'hotel_country', 'hotel_city', 'hotel_street',
                    'hotel_photo', 'time_create', 'is_published')
    list_filter = ('is_published', 'hotel_country', 'hotel_city')
    search_fields = ('hotel_name', 'hotel_country__country_name', 'hotel_city')

    def __str__(self):
        return self.country_name
