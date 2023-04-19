from django.contrib import admin
from .models import Hotels, HotelsImage
from django import forms
from core.models import Countries

# Register your models here.
class HotelForm(forms.ModelForm):
     hotel_country = forms.ModelChoiceField(queryset=Countries.objects.all())

     class Meta:
         model = Hotels
         fields = '__all__'

class HotelImageInline(admin.TabularInline):
    model = HotelsImage
    extra = 3

@admin.register(Hotels)
class HotelsAdmin(admin.ModelAdmin):
    form = HotelForm
    list_display = ('hotel_name', 'hotel_country', 'hotel_city', 'hotel_street',
                    'hotel_cover_photo', 'time_create', 'is_published')
    list_filter = ('is_published', 'hotel_country', 'hotel_city')
    search_fields = ('hotel_name', 'hotel_country__country_name', 'hotel_city')
    inlines = [ HotelImageInline, ]

    def __str__(self):
        return self.hotel_name


