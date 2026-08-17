from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail
from book_reading.models import Revise
from writing_plan.models import WritingPlan
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


@csrf_exempt
@require_GET
def send_daily_reminders(request):
    token = request.GET.get("token")
    if token != settings.REMINDER_TASK_TOKEN:
        return HttpResponseForbidden("Invalid token")

    today = timezone.localdate()

    revises = list(Revise.objects.filter(
        possible_date=today).order_by("order"))
    plans = list(WritingPlan.objects.filter(possible_date=today))

    for r in revises:
        r.priority_label = r.get_priority_display()
    for p in plans:
        p.priority_label = p.get_priority_display()

    if not revises and not plans:
        return JsonResponse({"status": "ok", "message": "Nothing due today."})

    html_content = render_to_string("emails/daily_reminder.html", {
        "today": today.strftime("%B %d, %Y"),
        "revises": revises,
        "plans": plans,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=f"Study Reminder - {today.strftime('%B %d, %Y')}",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=["sadiulhakim@gmail.com"],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    return JsonResponse({"status": "ok", "message": "Reminder email sent."})
