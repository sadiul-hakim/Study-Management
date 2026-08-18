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
import random
from general.models import WordCollection


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
        to=settings.REMINDER_EMAIL_TO,
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    return JsonResponse({"status": "ok", "message": "Reminder email sent."})


@csrf_exempt
@require_GET
def send_daily_words(request):
    token = request.GET.get("token")
    if token != settings.REMINDER_TASK_TOKEN:
        return HttpResponseForbidden("Invalid token")

    total = WordCollection.objects.count()
    if total == 0:
        return JsonResponse({"status": "ok", "message": "No words in collection."})

    sample_size = min(10, total)
    # Efficient random sampling without ORDER BY RANDOM() table scan
    ids = list(WordCollection.objects.values_list("id", flat=True))
    random_ids = random.sample(ids, sample_size)
    words = list(WordCollection.objects.filter(id__in=random_ids))
    random.shuffle(words)  # filter() doesn't preserve the random order

    for w in words:
        w.status_label = w.get_status_display()

    today = timezone.localdate()

    html_content = render_to_string("emails/daily_words.html", {
        "today": today.strftime("%B %d, %Y"),
        "words": words,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=f"Daily Word Practice - {today.strftime('%B %d, %Y')}",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.WORD_MEANING_EMAIL_TO,
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    return JsonResponse({"status": "ok", "message": f"{len(words)} words sent."})
