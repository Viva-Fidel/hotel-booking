from django.contrib import admin
from nested_admin import NestedTabularInline, NestedStackedInline, NestedModelAdmin
from .models import Hotels, Booking, Room, RoomTypeBed, HotelsImage, HotelsSearchInfo, HotelFacilities, HotelActivities, RoomType
from django import forms
from smart_selects.form_fields import ChainedModelChoiceField
from core.models import Counties

# Register your models here.


class HotelForm(forms.ModelForm):
    hotel_county = forms.ModelChoiceField(queryset=Counties.objects.all())

    class Meta:
        model = Hotels
        fields = '__all__'


class HotelsSearchInfoInlice(NestedStackedInline):
    model = HotelsSearchInfo
    extra = 1
    max_num = 1

class HotelImageInline(NestedTabularInline):
    model = HotelsImage
    extra = 3
    max_num = 3


class HotelFacilitiesInline(NestedStackedInline):
    model = HotelFacilities
    extra = 1
    max_num = 1


class HotelActivitiesInline(NestedStackedInline):
    model = HotelActivities
    extra = 1
    max_num = 1


class RoomTypeBedInline(NestedStackedInline):
    model = RoomTypeBed
    extra = 1
    max_num = 1


class RoomInline(NestedStackedInline):
    model = RoomType
    extra = 1
    inlines = [RoomTypeBedInline]


@admin.register(Hotels)
class HotelsAdmin(NestedModelAdmin):
    form = HotelForm
    list_display = ('hotel_name', 'hotel_type', 'hotel_star_rating', 'hotel_county', 'hotel_city', 'hotel_street',
                    'hotel_cover_photo', 'user_rating', 'time_create', 'is_published')
    list_filter = ('is_published', 'hotel_county', 'hotel_city')
    search_fields = ('hotel_name', 'hotel_county__county_name', 'hotel_city')
    inlines = [HotelsSearchInfoInlice, HotelImageInline, HotelFacilitiesInline,
               HotelActivitiesInline, RoomInline]

    exclude = ('hotel_popularity',)
    def __str__(self):
        return self.hotel_name

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 1
    fields = ['check_in_date', 'check_out_date', 'guest_count']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    fields = ['hotel', 'room_type', 'room_number', 'notes', 'available']
    list_display = ['hotel', 'room_type', 'room_number',]
    search_fields = ['hotel__name', 'room_type__name', 'room_number']
    list_filter = ['hotel', 'room_type']
    smart_selects = ('hotel',)
    inlines = [BookingInline]
