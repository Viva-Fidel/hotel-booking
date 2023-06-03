from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from .models import Hotels

@receiver(post_save, sender=Hotels)
def set_random_top_pick(sender, instance, created, **kwargs):
    if created and not instance.is_top_pick:
        # Set is_top_pick randomly with a 25% probability
        instance.is_top_pick = random.random() < 0.25
        instance.save()