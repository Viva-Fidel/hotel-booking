from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from core.models import Countries
import os

# Create your models here.


def cover_hotel_photo_path(instance, filename):
    return os.path.join('static/images/hotels', instance.hotel_name, 'cover', filename)


def hotel_general_photos_path(instance, filename):
    return os.path.join('static/images/hotels', instance.hotel_list.hotel_name, 'general', filename)



class Hotels(models.Model):
    hotel_name = models.CharField(max_length=255, verbose_name="Hotel name")
    hotel_country = models.ForeignKey(
        Countries, on_delete=models.CASCADE, verbose_name="Hotel country")
    hotel_city = models.CharField(
        max_length=255, verbose_name="Hotel city")
    hotel_street = models.CharField(
        max_length=255, verbose_name="Hotel street")
    hotel_zip_code = models.CharField(
        max_length=10, verbose_name="Hotel Zip code")
    hotel_description = models.TextField(verbose_name="Hotel overview")
    hotel_has_free_wifi = models.BooleanField(
        default=False, verbose_name="Free wifi")
    hotel_has_air_conditioning = models.BooleanField(
        default=False, verbose_name="Air Conditioning")
    hotel_has_parking_available = models.BooleanField(
        default=False, verbose_name="Parking available")
    hotel_has_business_services = models.BooleanField(
        default=False, verbose_name="Business Services")
    hotel_has_swimming_pool = models.BooleanField(
        default=False, verbose_name="Swimming pool")
    hotel_has_top_rated_in_area = models.BooleanField(
        default=False, verbose_name="Top rated in area")
    hotel_has_flat_screen_tv = models.BooleanField(
        default=False, verbose_name="Flat-screen TV")
    hotel_has_24_hour_front_desk = models.BooleanField(
        default=False, verbose_name="24-hour front desk")
    hotel_has_non_smoking_rooms = models.BooleanField(
        default=False, verbose_name="Non-smoking rooms")
    hotel_has_fitness_center = models.BooleanField(
        default=False, verbose_name="Fitness center")
    hotel_has_room_service = models.BooleanField(
        default=False, verbose_name="Room service")
    hotel_has_restaurant = models.BooleanField(
        default=False, verbose_name="Restaurant")
    hotel_is_pet_friendly = models.BooleanField(
        default=False, verbose_name="Pet friendly")
    hotel_has_facilities_for_disabled_guests = models.BooleanField(
        default=False, verbose_name="Facilities for disabled guests")
    hotel_has_family_rooms = models.BooleanField(
        default=False, verbose_name="Family rooms")
    hotel_has_spa = models.BooleanField(default=False, verbose_name="Spa")
    hotel_has_airport_shuttle = models.BooleanField(
        default=False, verbose_name="Airport shuttle")
    hotel_has_electric_vehicle_charging_station = models.BooleanField(
        default=False, verbose_name="Electric vehicle charging station")
    hotel_cover_photo = models.ImageField(
        upload_to=cover_hotel_photo_path, verbose_name="Hotel cover photo")
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Date of creation")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Updated")
    is_published = models.BooleanField(
        default=True, verbose_name="Is published")

    def __str__(self):
        return self.hotel_name


    class Meta:
        verbose_name = "Hotels"
        verbose_name_plural = "Hotels"
        ordering = ["hotel_name", "time_create"]

class HotelsImage(models.Model):
    hotel = models.ForeignKey(Hotels, related_name='general_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=hotel_general_photos_path, verbose_name="Hotel general photo")

    class Meta:
        verbose_name_plural = 'Hotels general photos'