from django.db import models

# Create your models here.

class Blog_post(models.Model):
    blog_title = models.CharField(max_length=255, verbose_name="Title")
    blog_text = models.TextField(verbose_name="Text")
    blog_photo = models.ImageField(upload_to="'static/images/blog")
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Date of creation")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Updated")
    is_published = models.BooleanField(
        default=True, verbose_name="Is publised")

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["blog_title", "time_create"]