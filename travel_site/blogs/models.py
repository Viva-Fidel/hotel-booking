from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class Blogs(models.Model):
    blog_title = models.CharField(max_length=255, verbose_name="Title")
    blog_text = models.TextField(verbose_name="Text")
    blog_photo = models.ImageField(upload_to="static/images/blog")
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

        
