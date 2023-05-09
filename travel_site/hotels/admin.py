from django.contrib import admin
from .models import Hotels, HotelsImage, HotelFacilities, HotelActivities, Room, RoomType, BedType
from django import forms
from core.models import Counties

# Register your models here.


class HotelForm(forms.ModelForm):
    hotel_county = forms.ModelChoiceField(queryset=Counties.objects.all())

    class Meta:
        model = Hotels
        fields = '__all__'


class HotelImageInline(admin.TabularInline):
    model = HotelsImage
    extra = 3


class HotelFacilitiesInline(admin.StackedInline):
    model = HotelFacilities
    extra = 1


class HotelActivitiesInline(admin.StackedInline):
    model = HotelActivities
    extra = 1


class RoomTypeInline(admin.StackedInline):
    model = RoomType
    extra = 1


@admin.register(Hotels)
class HotelsAdmin(admin.ModelAdmin):
    form = HotelForm
    list_display = ('hotel_name', 'hotel_county', 'hotel_city', 'hotel_street',
                    'hotel_cover_photo', 'time_create', 'is_published')
    list_filter = ('is_published', 'hotel_county', 'hotel_city')
    search_fields = ('hotel_name', 'hotel_county__county_name', 'hotel_city')
    inlines = [HotelImageInline, HotelFacilitiesInline, HotelActivitiesInline,
               RoomTypeInline, ]
    exclude = ('hotel_popularity', 'hotel_rating',)

    def __str__(self):
        return self.hotel_name
