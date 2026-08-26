import logging
from django.core.management.base import BaseCommand
from general.tasks import send_daily_reminders_task, send_daily_words_task

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Dispatches daily revision reminders and daily vocabulary words"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Running daily reminder task..."))
        reminder_res = send_daily_reminders_task()
        self.stdout.write(f"Reminder Result: {reminder_res}")

        self.stdout.write(self.style.NOTICE("Running daily words task..."))
        words_res = send_daily_words_task()
        self.stdout.write(f"Words Result: {words_res}")

        self.stdout.write(self.style.SUCCESS("All daily tasks completed."))
