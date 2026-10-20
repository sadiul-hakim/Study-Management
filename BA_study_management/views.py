from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render

from general.tasks import send_daily_reminders_task, send_daily_words_task


from general.models import Notes


def home(request):
    sticky_notes = Notes.objects.filter(show_on_home_page=True).order_by("order")
    return render(request, "home.html", {"sticky_notes": sticky_notes})



@csrf_exempt
@require_GET
def send_daily_reminders(request):
    token = request.GET.get("token")
    if not settings.REMINDER_TASK_TOKEN or token != settings.REMINDER_TASK_TOKEN:
        return HttpResponseForbidden("Invalid token")

    # Run asynchronously by default so WSGI worker on PythonAnywhere is freed immediately (<10ms).
    # Pass ?sync=true to run synchronously and wait for full execution.
    sync_mode = request.GET.get("sync", "false").lower() in ("1", "true")
    result = send_daily_reminders_task(run_async_mode=not sync_mode)
    return JsonResponse(result)


@csrf_exempt
@require_GET
def send_daily_words(request):
    token = request.GET.get("token")
    if not settings.REMINDER_TASK_TOKEN or token != settings.REMINDER_TASK_TOKEN:
        return HttpResponseForbidden("Invalid token")

    # Run asynchronously by default so WSGI worker on PythonAnywhere is freed immediately (<10ms).
    # Pass ?sync=true to run synchronously and wait for full execution.
    sync_mode = request.GET.get("sync", "false").lower() in ("1", "true")
    result = send_daily_words_task(run_async_mode=not sync_mode)
    return JsonResponse(result)

