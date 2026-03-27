from django.conf import settings
from django.core.cache import cache


def _cache_ttl() -> int:
    return int(getattr(settings, "IMAGE_URL_CACHE_TTL", 3600))


def build_image_cache_key(model_label: str, pk: int, field_name: str) -> str:
    return f"image-url:{model_label}:{pk}:{field_name}"


def get_cached_image_url(obj, field_name: str = "image", fallback: str = "") -> str:
    if not obj or not getattr(obj, field_name, None):
        return fallback

    if not getattr(obj, "pk", None):
        return fallback

    cache_key = build_image_cache_key(obj._meta.label_lower, obj.pk, field_name)
    cached_url = cache.get(cache_key)
    if cached_url:
        return cached_url

    try:
        url = getattr(obj, field_name).url
    except Exception:
        return fallback

    cache.set(cache_key, url, _cache_ttl())
    return url


def invalidate_cached_image(obj, field_name: str = "image") -> None:
    if not obj or not getattr(obj, "pk", None):
        return

    cache_key = build_image_cache_key(obj._meta.label_lower, obj.pk, field_name)
    cache.delete(cache_key)
