from .models import ReadingPlan, ReadingProgress, Revise


def admin_reading_plan(request):
    reading_plan = ReadingPlan.objects.order_by("priority").all() or False
    return {"reading_plan": reading_plan if reading_plan is not False else None}


def admin_revise(request):
    revise = Revise.objects.order_by("priority").all() or False
    return {"revise": revise if revise is not False else None}


def admin_reading_progress(request):
    reading_progress = ReadingProgress.objects.all() or False
    return {
        "reading_progress": reading_progress if reading_progress is not False else None
    }
