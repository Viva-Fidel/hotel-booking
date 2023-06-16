# Generated by Django 4.2 on 2023-06-16 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0016_room_price_per_night'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='price_per_night',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Price per night of the room type', max_digits=8),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='price_per_night',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Price per night of the room type', max_digits=8),
        ),
    ]
