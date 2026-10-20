from django.core.cache import cache
from .models import Guide


def admin_guide(request):
    guide = cache.get("admin_guide_cached")
    if guide is None:
        guide = Guide.objects.order_by("-priority").first() or False
        cache.set("admin_guide_cached", guide, timeout=300)
    return {
        "guide": guide if guide is not False else None
    }
