from django.db import models
import os

# Create your models here.


def hotel_photo_path(instance, filename):
    # Generate upload path based on hotel name
    return os.path.join('static/images/', instance.hotel_name, filename)


class Hotel_list(models.Model):
    hotel_name = models.CharField(max_length=255, verbose_name="Hotel name")
    hotel_country = models.CharField(
        max_length=255, verbose_name="Hotel country")
    hotel_city = models.CharField(
        max_length=255, verbose_name="Hotel city")
    hotel_street = models.CharField(
        max_length=255, verbose_name="Hotel street")
    hotel_description = models.TextField(verbose_name="Hotel overview")
    hotel_facilities = models.CharField(
        max_length=255, verbose_name="Hotel facilities")
    hotel_photo = models.ImageField(upload_to=hotel_photo_path)
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Date of creation")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Updated")
    is_published = models.BooleanField(
        default=True, verbose_name="Is publised")

    class Meta:
        verbose_name = "Hotels"
        verbose_name_plural = "Hotels"
        ordering = ["hotel_name", "time_create"]
