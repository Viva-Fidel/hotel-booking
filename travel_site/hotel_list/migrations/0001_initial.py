# Generated by Django 4.2 on 2023-04-11 09:00

from django.db import migrations, models
import hotel_list.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=255, verbose_name='Hotel name')),
                ('hotel_country', models.CharField(max_length=255, verbose_name='Hotel address')),
                ('hotel_city', models.CharField(max_length=255, verbose_name='Hotel city')),
                ('hotel_street', models.CharField(max_length=255, verbose_name='Hotel street')),
                ('hotel_description', models.TextField(verbose_name='Hotel overview')),
                ('hotel_facilities', models.CharField(max_length=255, verbose_name='Hotel facilities')),
                ('hotel_photo', models.ImageField(upload_to=hotel_list.models.hotel_photo_path)),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('is_published', models.BooleanField(default=True, verbose_name='Is publised')),
            ],
            options={
                'verbose_name': 'Hotels',
                'verbose_name_plural': 'Hotels',
                'ordering': ['hotel_name', 'time_create'],
            },
        ),
    ]
