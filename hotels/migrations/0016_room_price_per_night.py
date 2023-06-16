# Generated by Django 4.2 on 2023-06-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0015_room_max_guests'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='price_per_night',
            field=models.DecimalField(decimal_places=2, default=None, help_text='Price per night of the room type', max_digits=8),
        ),
    ]
