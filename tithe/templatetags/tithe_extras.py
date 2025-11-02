from django import template

register = template.Library()

@register.filter
def avg_tithe(queryset):
    """Calculate the average tithe amount from a queryset."""
    amounts = [getattr(obj, 'amount', 0) for obj in queryset if hasattr(obj, 'amount')]
    if not amounts:
        return 0
    return round(sum(amounts) / len(amounts), 2)
