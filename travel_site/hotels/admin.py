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
    inlines = [ HotelImageInline, HotelFacilitiesInline, HotelActivitiesInline,
                RoomTypeInline, ]
    exclude = ('hotel_popularity', 'hotel_rating',)

    def __str__(self):
        return self.hotel_name



# class RoomForm(forms.ModelForm):
#     hotel = forms.ModelChoiceField(queryset=Hotels.objects.all())
#     room_number = forms.CharField(max_length=50)
#     notes = forms.CharField(widget=forms.Textarea)
#     available = forms.BooleanField()

#     class Meta:
#         model = Room
#         fields = ['hotel', 'room_type', 'room_number', 'notes', 'available']

#     def __init__(self, *args, **kwargs):
#         super(RoomForm, self).__init__(*args, **kwargs)
#         if 'instance' in kwargs:
#             instance = kwargs['instance']
#             self.fields['room_type'].queryset = RoomType.objects.filter(hotel=instance.hotel)
#         elif 'initial' in kwargs and 'hotel' in kwargs['initial']:
#             hotel = kwargs['initial']['hotel']
#             self.fields['room_type'].queryset = RoomType.objects.filter(hotel=hotel)
#         else:
#             self.fields['room_type'].queryset = RoomType.objects.none()

# @admin.register(Room)
# class RoomAdmin(admin.ModelAdmin):
#     form = RoomForm
#     list_display = ('room_number', 'room_type', 'available')
#     list_filter = ('available',)
#     search_fields = ('room_number', 'room_type__room_type_name', 'room_type__hotel__hotel_name')


# @admin.register(BedType)
# class BedTypeAdmin(admin.ModelAdmin):
#     list_display = ['beds', 'bed_types']

# class RoomInline(admin.TabularInline):
#     model = Room
#     extra = 1

# @admin.register(RoomType)
# class RoomTypeAdmin(admin.ModelAdmin):
#     list_display = ['name', 'description', 'price_per_night']
#     inlines = [RoomInline]
#     search_fields = ['name', 'description']

# @admin.register(Room)
# class RoomAdmin(admin.ModelAdmin):
#     list_display = ['room_number', 'available', 'room_type', 'notes']
#     list_filter = ['available', 'room_type__name']
#     search_fields = ['room_number', 'room_type__name', 'notes']



