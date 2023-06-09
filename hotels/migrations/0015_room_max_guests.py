# Generated by Django 4.2 on 2023-06-09 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0014_remove_room_max_guests_roomtype_max_guests'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='max_guests',
            field=models.PositiveIntegerField(default=0, help_text='Maximum number of guests'),
        ),
    ]
