# Generated by Django 4.2 on 2023-06-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_counties_county_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counties',
            name='county_name',
            field=models.CharField(help_text='Add a county name', max_length=25, verbose_name='County name'),
        ),
        migrations.AlterField(
            model_name='cover',
            name='cover_photo',
            field=models.ImageField(help_text='Set a photo cover in the main page', upload_to='images/core/cover_photo', verbose_name='Cover photo'),
        ),
        migrations.AlterField(
            model_name='cover',
            name='cover_text',
            field=models.TextField(help_text='Set a text for the cover in the main page', max_length=255, verbose_name='Cover text'),
        ),
        migrations.AlterField(
            model_name='cover',
            name='cover_title',
            field=models.CharField(help_text='Set a title for the cover in the main page', max_length=50, verbose_name='Cover title'),
        ),
    ]
