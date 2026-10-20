import logging
import random
import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import close_old_connections
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from book_reading.models import Revise
from writing_plan.models import WritingPlan
from vocabulary.models import WordCollection

logger = logging.getLogger(__name__)


def run_async(task_func, *args, **kwargs):
    """
    Executes a task in a lightweight background daemon thread.
    Properly handles Django DB connections before and after execution to prevent
    connection leaks or database locking on memory-constrained environments
    like PythonAnywhere Free Tier.
    """
    def thread_runner():
        close_old_connections()
        try:
            task_func(*args, **kwargs)
        except Exception as exc:
            func_name = getattr(task_func, "__name__", str(task_func))
            logger.error(f"Async background task {func_name} failed: {exc}", exc_info=True)
        finally:
            close_old_connections()

    thread = threading.Thread(
        target=thread_runner,
        name=f"TaskThread-{getattr(task_func, '__name__', 'worker')}",
        daemon=True,
    )
    thread.start()
    return thread


def _send_daily_reminders_exec():
    """Internal execution logic for daily reminders."""
    try:
        today = timezone.localdate()

        revises = list(
            Revise.objects.filter(possible_date=today)
            .select_related("book", "chapter")
            .order_by("order")
        )
        plans = list(
            WritingPlan.objects.filter(possible_date=today)
            .select_related("book", "chapter")
        )

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


def send_daily_reminders_task(run_async_mode: bool = False):
    """
    Task to send daily study & writing plan reminders due today.
    If run_async_mode=True, dispatches to a background thread and returns immediately.
    """
    if run_async_mode:
        run_async(_send_daily_reminders_exec)
        return {"status": "queued", "message": "Daily reminder task queued in background."}
    return _send_daily_reminders_exec()


def send_daily_reminders_async():
    """Convenience alias to dispatch daily reminders asynchronously."""
    return send_daily_reminders_task(run_async_mode=True)


def _send_daily_words_exec():
    """Internal execution logic for sending daily vocabulary words."""
    try:
        total = WordCollection.objects.count()
        if total == 0:
            logger.info("send_daily_words_task: No words in collection.")
            return {"status": "ok", "message": "No words in collection."}

        sample_size = min(10, total)
        ids = list(WordCollection.objects.values_list("id", flat=True))
        random_ids = random.sample(ids, sample_size)
        words = list(
            WordCollection.objects.filter(id__in=random_ids)
            .only("id", "english", "bengali", "status")
        )
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


def send_daily_words_task(run_async_mode: bool = False):
    """
    Task to send 10 random vocabulary practice words.
    If run_async_mode=True, dispatches to a background thread and returns immediately.
    """
    if run_async_mode:
        run_async(_send_daily_words_exec)
        return {"status": "queued", "message": "Daily words practice task queued in background."}
    return _send_daily_words_exec()


def send_daily_words_async():
    """Convenience alias to dispatch daily words practice asynchronously."""
    return send_daily_words_task(run_async_mode=True)

