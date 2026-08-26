import logging
import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings

logger = logging.getLogger(__name__)

_scheduler = None


def start():
    """Starts the in-process background scheduler."""
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        return

    # Avoid duplicate scheduler execution in development when Django's auto-reloader runs
    if "runserver" in sys.argv and os.environ.get("RUN_MAIN") != "true":
        return

    # Avoid running scheduler during management commands like migrate, makemigrations, collectstatic
    ignored_commands = ["makemigrations", "migrate", "test", "collectstatic", "shell"]
    if any(cmd in sys.argv for cmd in ignored_commands):
        return

    from .tasks import send_daily_reminders_task, send_daily_words_task

    tz = getattr(settings, "TIME_ZONE", "Asia/Dhaka")
    task_time_str = getattr(settings, "DAILY_TASK_TIME", "19:00").strip()

    try:
        if ":" in task_time_str:
            task_hour, task_minute = map(int, task_time_str.split(":", 1))
        else:
            task_hour, task_minute = int(task_time_str), 0
    except (ValueError, TypeError):
        task_hour, task_minute = 19, 0

    _scheduler = BackgroundScheduler(timezone=tz)

    # Schedule Daily Reminders
    _scheduler.add_job(
        send_daily_reminders_task,
        trigger=CronTrigger(hour=task_hour, minute=task_minute, timezone=tz),
        id="send_daily_reminders_job",
        name=f"Daily study & writing plan reminders at {task_hour:02d}:{task_minute:02d}",
        replace_existing=True,
    )

    # Schedule Daily Words
    _scheduler.add_job(
        send_daily_words_task,
        trigger=CronTrigger(hour=task_hour, minute=task_minute, timezone=tz),
        id="send_daily_words_job",
        name=f"Daily vocabulary practice words at {task_hour:02d}:{task_minute:02d}",
        replace_existing=True,
    )

    try:
        _scheduler.start()
        logger.info(
            f"APScheduler active: daily reminders & words scheduled at {task_hour:02d}:{task_minute:02d} [{tz}]."
        )
    except Exception as e:
        logger.error(f"Failed to start APScheduler: {e}", exc_info=True)

