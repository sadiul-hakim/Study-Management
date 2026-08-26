import logging
import random
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from book_reading.models import Revise
from writing_plan.models import WritingPlan
from vocabulary.models import WordCollection

logger = logging.getLogger(__name__)


def send_daily_reminders_task():
    """Task to send daily study & writing plan reminders due today."""
    try:
        today = timezone.localdate()

        revises = list(Revise.objects.filter(possible_date=today).order_by("order"))
        plans = list(WritingPlan.objects.filter(possible_date=today))

        for r in revises:
            r.priority_label = r.get_priority_display()
        for p in plans:
            p.priority_label = p.get_priority_display()

        if not revises and not plans:
            logger.info("send_daily_reminders_task: Nothing due today.")
            return {"status": "ok", "message": "Nothing due today."}

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

        logger.info(f"send_daily_reminders_task: Reminder email sent to {settings.REMINDER_EMAIL_TO}.")
        return {"status": "ok", "message": "Reminder email sent."}
    except Exception as e:
        logger.error(f"send_daily_reminders_task error: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def send_daily_words_task():
    """Task to send 10 random vocabulary practice words."""
    try:
        total = WordCollection.objects.count()
        if total == 0:
            logger.info("send_daily_words_task: No words in collection.")
            return {"status": "ok", "message": "No words in collection."}

        sample_size = min(10, total)
        ids = list(WordCollection.objects.values_list("id", flat=True))
        random_ids = random.sample(ids, sample_size)
        words = list(WordCollection.objects.filter(id__in=random_ids))
        random.shuffle(words)

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

        logger.info(f"send_daily_words_task: {len(words)} words sent to {settings.WORD_MEANING_EMAIL_TO}.")
        return {"status": "ok", "message": f"{len(words)} words sent."}
    except Exception as e:
        logger.error(f"send_daily_words_task error: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
