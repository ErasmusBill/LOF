from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from tithe.image_cache import invalidate_cached_image
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def invalidate_user_avatar_cache_on_save(sender, instance, **kwargs):
    invalidate_cached_image(instance, field_name="avatar")


@receiver(post_delete, sender=CustomUser)
def invalidate_user_avatar_cache_on_delete(sender, instance, **kwargs):
    invalidate_cached_image(instance, field_name="avatar")
