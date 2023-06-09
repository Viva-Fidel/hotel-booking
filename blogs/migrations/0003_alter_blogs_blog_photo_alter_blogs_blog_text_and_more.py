# Generated by Django 4.2 on 2023-06-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_alter_blogs_blog_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='blog_photo',
            field=models.ImageField(help_text='Add photo for the article', upload_to='images/blogs'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='blog_text',
            field=models.TextField(help_text='Write text for the article', verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='blog_title',
            field=models.CharField(help_text='Set title for the text', max_length=50, verbose_name='Title'),
        ),
    ]
