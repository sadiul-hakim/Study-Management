from .models import Guide


def admin_guide(request):
    return {
        "guide": Guide.objects.order_by("-priority").first()
    }
