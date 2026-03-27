from django import template

from tithe.image_cache import get_cached_image_url

register = template.Library()


@register.simple_tag
def cached_image_url(obj, field_name: str = "image", fallback: str = "") -> str:
    return get_cached_image_url(obj, field_name=field_name, fallback=fallback)
