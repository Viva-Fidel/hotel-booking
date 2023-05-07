import os

from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

# Create your models here.


class Counties(models.Model):
    county_name = models.CharField(
        max_length=25, verbose_name="County name")
    county_photo = models.ImageField(upload_to="images/core/county_photo")

    def __str__(self):
        return self.county_name

    class Meta:
        verbose_name = "County"
        verbose_name_plural = "Counties"
        ordering = ["county_name"]


class Cover(models.Model):
    cover_title = models.CharField(
        max_length=255, verbose_name="Cover title")
    cover_text = models.TextField(
        max_length=255, verbose_name="Cover text")
    cover_photo = models.ImageField(
        upload_to="images/core/cover_photo", verbose_name="Cover photo")

    def __str__(self):
        return self.cover_title

    class Meta:
        verbose_name = "Manage cover"

# A signal to delete the previous county photo when a new one is uploaded


@receiver(pre_save, sender=Counties)
def delete_previous_county_photo(sender, instance, **kwargs):
    try:
        # Get the old cover photo of the instance
        old_county_photo = sender.objects.get(pk=instance.pk).county_photo
    except sender.DoesNotExist:
        # If the instance doesn't exist, do nothing
        return

    # Get the new cover photo of the instance
    new_county_photo = instance.county_photo
    # If the old and new county photos are not the same, delete the old county photo
    if old_county_photo and not old_county_photo == new_county_photo:
        old_county_photo.delete(save=False)


@receiver(post_delete, sender=Counties)
def auto_delete_county_file_on_delete(sender, instance, **kwargs):
    if instance.county_photo:
        if os.path.isfile(instance.county_photo.path):
            # If the file exists, delete it from the storage
            os.remove(instance.county_photo.path)


# A signal to delete the previous cover photo when a new one is uploaded
@receiver(pre_save, sender=Cover)
def delete_previous_cover_photo(sender, instance, **kwargs):
    try:
        # Get the old cover photo of the instance
        old_cover_photo = sender.objects.get(pk=instance.pk).cover_photo
    except sender.DoesNotExist:
        # If the instance doesn't exist, do nothing
        return

    # Get the new cover photo of the instance
    new_cover_photo = instance.cover_photo
    # If the old and new cover photos are not the same, delete the old cover photo
    if not old_cover_photo == new_cover_photo:
        old_cover_photo.delete(save=False)


# A signal to delete the file from the storage when a Cover instance is deleted
@receiver(post_delete, sender=Cover)
def auto_delete_file_on_delete(instance, **kwargs):
    if instance.cover_photo:
        # Check if the file still exists in the storage
        if os.path.isfile(instance.cover_photo.path):
            # If the file exists, delete it from the storage
            os.remove(instance.cover_photo.path)
