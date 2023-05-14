# Generated by Django 4.2 on 2023-05-11 13:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hotels.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_counties_county_name'),
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotelsimage',
            options={'verbose_name': 'Hotel general photo'},
        ),
        migrations.AddField(
            model_name='hotels',
            name='hotel_type',
            field=models.CharField(choices=[('hotel', 'Hotel'), ('apartment', 'Apartment'), ('residence', 'Residence'), ('resort', 'Resort'), ('shared_space', 'Shared Space')], default=None, help_text='Allocation type', max_length=50, verbose_name='Allocation type'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='hotel_city',
            field=models.CharField(help_text='Hotel city', max_length=255, verbose_name='Hotel city'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='hotel_county',
            field=models.ForeignKey(help_text='Hotel county', on_delete=django.db.models.deletion.CASCADE, to='core.counties', verbose_name='Hotel county'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='hotel_cover_photo',
            field=models.ImageField(help_text='Hotel main photo', upload_to=hotels.models.cover_hotel_photo_path, verbose_name='Hotel cover photo'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='hotel_description',
            field=models.TextField(help_text='Hotel description', verbose_name='Hotel overview'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='hotel_name',
            field=models.CharField(help_text='Hotel name', max_length=255, verbose_name='Hotel name'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='hotel_street',
            field=models.CharField(help_text='Hotel street', max_length=255, verbose_name='Hotel street'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='hotel_zip_code',
            field=models.CharField(help_text='Hotel Zip code', max_length=10, verbose_name='Hotel Zip code'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Is the hotel currently available?', verbose_name='Is published'),
        ),
        migrations.AlterField(
            model_name='hotelsimage',
            name='image',
            field=models.ImageField(help_text='General photos of the hotel', upload_to=hotels.models.hotel_general_photos_path, verbose_name='Hotel general photos'),
        ),
        migrations.CreateModel(
            name='RoomDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_discount', models.IntegerField(help_text='Discount percentage', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('special_discount', models.CharField(blank=True, help_text='Special discount (optional)', max_length=50)),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='hotels.roomtype')),
            ],
        ),
        migrations.CreateModel(
            name='HotelsSearchInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_search_info_title', models.CharField(help_text='Hotel description title for search page', max_length=50, verbose_name='Hotel serach page title')),
                ('hotel_search_info_text', models.CharField(help_text='Hotel description text for search page', max_length=120, verbose_name='Hotel serach page text')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_search_info', to='hotels.hotels')),
            ],
            options={
                'verbose_name': 'Information about the hotel for the search page',
            },
        ),
    ]
