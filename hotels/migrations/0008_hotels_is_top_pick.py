# Generated by Django 4.2 on 2023-06-03 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0007_rename_hotel_is_pet_friendly_hotelfacilities_hotel_has_pet_friendly'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotels',
            name='is_top_pick',
            field=models.BooleanField(default=False, verbose_name='Is Top Pick'),
        ),
    ]
