from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Hotels

from decimal import Decimal
import random

@receiver(post_save, sender=Hotels)
def set_random_fields(sender, instance, created, **kwargs):
    if created and not instance.is_top_pick:
        # Set is_top_pick randomly with a 25% probability
        instance.is_top_pick = random.random() < 0.25
    
    if created and not instance.amount_of_reviews:
        # Generate a random value between 1 and 1000 for amount_of_reviews
        instance.amount_of_reviews = random.randint(1, 1000)
    
    if created and instance.user_rating == Decimal('0.00'):
        # Generate a random rating between 0.00 and 5.00
        instance.user_rating = round(random.uniform(0.00, 5.00), 2)
    
    instance.__class__.objects.filter(pk=instance.pk).update(
        is_top_pick=instance.is_top_pick,
        amount_of_reviews=instance.amount_of_reviews,
        user_rating=instance.user_rating
    )


@receiver(post_save, sender=Hotels)
def update_recommendation_score(sender, instance, created, **kwargs):
    if created and not instance.recommended_score:
        # Calculate the recommendation score based on different factors
        popularity_factor = Decimal(instance.hotel_popularity) / 100
        rating_factor = Decimal(instance.user_rating) / 5
        star_rating_factor = Decimal(instance.hotel_star_rating) / 5
        top_pick_factor = Decimal(1) if instance.is_top_pick else Decimal(0)
        reviews_factor = Decimal(instance.amount_of_reviews) / 1000

        # Calculate the recommended_score
        recommended_score = (
            popularity_factor * Decimal('0.3') +
            rating_factor * Decimal('0.2') +
            star_rating_factor * Decimal('0.2') +
            top_pick_factor * Decimal('0.1') +
            reviews_factor * Decimal('0.2')
        )

        # Set the calculated recommended_score
        instance.__class__.objects.filter(pk=instance.pk).update(
            recommended_score=round(recommended_score, 2)
        )
