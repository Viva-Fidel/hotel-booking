from django.db import models

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
