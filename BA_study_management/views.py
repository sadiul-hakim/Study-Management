from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render

from general.tasks import send_daily_reminders_task, send_daily_words_task


def home(request):
    return render(request, "home.html")


@csrf_exempt
@require_GET
def send_daily_reminders(request):
    token = request.GET.get("token")
    if token != settings.REMINDER_TASK_TOKEN:
        return HttpResponseForbidden("Invalid token")

    result = send_daily_reminders_task()
    return JsonResponse(result)


@csrf_exempt
@require_GET
def send_daily_words(request):
    token = request.GET.get("token")
    if token != settings.REMINDER_TASK_TOKEN:
        return HttpResponseForbidden("Invalid token")

    result = send_daily_words_task()
    return JsonResponse(result)

