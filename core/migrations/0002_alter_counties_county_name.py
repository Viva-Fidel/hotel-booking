# Generated by Django 4.2 on 2023-05-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counties',
            name='county_name',
            field=models.CharField(max_length=25, verbose_name='County name'),
        ),
    ]
