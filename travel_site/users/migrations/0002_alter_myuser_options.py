# Generated by Django 4.2 on 2023-05-11 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'ordering': ['last_login'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
