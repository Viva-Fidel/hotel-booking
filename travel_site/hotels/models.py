from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from core.models import Countries
import os

# Create your models here.


def cover_hotel_photo_path(instance, filename):
    return os.path.join('static/images/hotels', instance.hotel_name, 'cover', filename)


def hotel_general_photos_path(instance, filename):
    return os.path.join('static/images/hotels', instance.hotel.hotel_name, 'general', filename)


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
    hotel_cover_photo = models.ImageField(
        upload_to=cover_hotel_photo_path, verbose_name="Hotel cover photo")
    hotel_popularity = models.PositiveIntegerField(default=0)
    hotel_rating = models.DecimalField(decimal_places=2, max_digits=5, default=0.00)
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
    hotel = models.ForeignKey(
        Hotels, related_name='general_images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=hotel_general_photos_path, verbose_name="Hotel general photo")

    class Meta:
        verbose_name_plural = 'Hotels general photos'


class HotelFacilities(models.Model):
    facilities = models.ForeignKey(
        Hotels, related_name='hotel_facilities', on_delete=models.CASCADE)
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
    hotel_has_free_cancellation = models.BooleanField(
        default=False, verbose_name="Free cancellation")
    hotel_has_beach_front = models.BooleanField(
        default=False, verbose_name="Beach front")
    hotel_has_jacuzzi = models.BooleanField(
        default=False, verbose_name="Hot tub/jacuzzi")
    hotel_has_without_credit_card = models.BooleanField(
        default=False, verbose_name="Book without credit card")
    hotel_has_no_prepayment = models.BooleanField(
        default=False, verbose_name="No prepayment")


class HotelActivities(models.Model):
    activities = models.ForeignKey(
        Hotels, related_name='hotel_activities', on_delete=models.CASCADE)
    hotel_has_fishing = models.BooleanField(
        default=False, verbose_name="Fishing")
    hotel_has_hiking = models.BooleanField(
        default=False, verbose_name="Hiking")
    hotel_has_beach = models.BooleanField(
        default=False, verbose_name="Beach")
    hotel_has_cycling = models.BooleanField(
        default=False, verbose_name="Cycling")
    hotel_has_sauna = models.BooleanField(
        default=False, verbose_name="Sauna")
    hotel_has_night_lights = models.BooleanField(
        default=False, verbose_name="Night lights")
    hotel_has_tennis = models.BooleanField(
        default=False, verbose_name="Tennis")
    hotel_has_yoga = models.BooleanField(
        default=False, verbose_name="Yoga")
    hotel_has_scuba_diving = models.BooleanField(
        default=False, verbose_name="Scuba diving")
    hotel_has_rafting = models.BooleanField(
        default=False, verbose_name="Rafting")
    hotel_has_guided_nature_walks = models.BooleanField(
        default=False, verbose_name="Guided nature walks")
    hotel_has_skiing = models.BooleanField(
        default=False, verbose_name="Skiing or snowboarding")
    hotel_has_golfing = models.BooleanField(
        default=False, verbose_name="Golfing")
    hotel_has_surfing = models.BooleanField(
        default=False, verbose_name="Surfing")
    
    