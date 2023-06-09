# Generated by Django 4.2 on 2023-06-09 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0013_roomtype_area'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='max_guests',
        ),
        migrations.AddField(
            model_name='roomtype',
            name='max_guests',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
