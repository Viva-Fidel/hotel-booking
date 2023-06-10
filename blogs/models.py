from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

import os

# Create your models here.


class Blogs(models.Model):
    blog_title = models.CharField(max_length=50, verbose_name="Title", help_text='Set title for the text')
    blog_text = models.TextField(verbose_name="Text", help_text='Write text for the article')
    blog_photo = models.ImageField(upload_to="images/blogs", help_text='Add photo for the article')
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Date of creation")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Updated")
    is_published = models.BooleanField(
        default=True, verbose_name="Is publised")
    slug = models.SlugField(max_length=255, unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.blog_title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])
    
    def __str__(self):
        return self.blog_title
    
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["blog_title", "time_create"]

        
# A signal to delete the previous blog photo when a new one is uploaded
@receiver(pre_save, sender=Blogs)
def delete_previous_blog_photo(sender, instance, **kwargs):
    try:
        # Get the old blog photo of the instance
        old_blog_photo = sender.objects.get(pk=instance.pk).blog_photo
    except sender.DoesNotExist:
        # If the instance doesn't exist, do nothing
        return

    # Get the new blog photo of the instance
    new_blog_photo = instance.blog_photo
    # If the old and new blog photos are not the same, delete the old blog photo
    if not old_blog_photo == new_blog_photo:
        old_blog_photo.delete(save=False)


# A signal to delete the file from the storage when a Blog instance is deleted
@receiver(post_delete, sender=Blogs)
def auto_delete_file_on_delete(instance, **kwargs):
    if instance.blog_photo:
        # Check if the file still exists in the storage
        if os.path.isfile(instance.blog_photo.path):
            # If the file exists, delete it from the storage
            os.remove(instance.blog_photo.path)