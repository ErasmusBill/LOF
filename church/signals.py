from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from tithe.image_cache import invalidate_cached_image
from .models import Event, Group, Leadership


@receiver(post_save, sender=Event)
def invalidate_event_image_cache_on_save(sender, instance, **kwargs):
    invalidate_cached_image(instance, field_name="image")


@receiver(post_delete, sender=Event)
def invalidate_event_image_cache_on_delete(sender, instance, **kwargs):
    invalidate_cached_image(instance, field_name="image")


@receiver(post_save, sender=Group)
def invalidate_group_image_cache_on_save(sender, instance, **kwargs):
    invalidate_cached_image(instance, field_name="image")


@receiver(post_delete, sender=Group)
def invalidate_group_image_cache_on_delete(sender, instance, **kwargs):
    invalidate_cached_image(instance, field_name="image")


@receiver(post_save, sender=Leadership)
def invalidate_leadership_image_cache_on_save(sender, instance, **kwargs):
    invalidate_cached_image(instance, field_name="image")


@receiver(post_delete, sender=Leadership)
def invalidate_leadership_image_cache_on_delete(sender, instance, **kwargs):
    invalidate_cached_image(instance, field_name="image")
