import os

from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

# Create your models here.


class Countries(models.Model):
    country_name = models.CharField(
        max_length=255, verbose_name="Country name")
    country_photo = models.ImageField(upload_to="static/images/country_photo")

    def __str__(self):
        return self.country_name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["country_name"]

class CoverPhoto(models.Model):
    cover_photo = models.ImageField(upload_to="static/images/cover_photo")

    def __str__(self):
        return self.cover_photo.name

    class Meta:
        verbose_name = "Cover Photo"
        verbose_name_plural = "Cover Photos"
    
@receiver(pre_save, sender=CoverPhoto)
def delete_previous_cover_photo(sender, instance, **kwargs):
    try:
        old_cover_photo = sender.objects.get(pk=instance.pk).cover_photo
    except sender.DoesNotExist:
        return

    new_cover_photo = instance.cover_photo
    if not old_cover_photo == new_cover_photo:
        old_cover_photo.delete(save=False)

@receiver(post_delete, sender=CoverPhoto)
def auto_delete_file_on_delete(instance, **kwargs):
    if instance.cover_photo:
        if os.path.isfile(instance.cover_photo.path):
            os.remove(instance.cover_photo.path)