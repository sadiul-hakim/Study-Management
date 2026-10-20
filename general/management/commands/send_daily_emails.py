import logging
from django.core.management.base import BaseCommand
from general.tasks import send_daily_reminders_task, send_daily_words_task

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Dispatches daily revision reminders and daily vocabulary words (Ideal for PythonAnywhere Scheduled Tasks)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reminders-only",
            action="store_true",
            help="Send only study and writing plan reminders",
        )
        parser.add_argument(
            "--words-only",
            action="store_true",
            help="Send only daily vocabulary practice words",
        )
        parser.add_argument(
            "--async",
            action="store_true",
            dest="async_mode",
            help="Dispatch tasks asynchronously in background threads",
        )

    def handle(self, *args, **options):
        reminders_only = options.get("reminders_only", False)
        words_only = options.get("words_only", False)
        async_mode = options.get("async_mode", False)

        if not words_only:
            self.stdout.write(self.style.NOTICE("Running daily reminder task..."))
            reminder_res = send_daily_reminders_task(run_async_mode=async_mode)
            self.stdout.write(f"Reminder Result: {reminder_res}")

        if not reminders_only:
            self.stdout.write(self.style.NOTICE("Running daily words task..."))
            words_res = send_daily_words_task(run_async_mode=async_mode)
            self.stdout.write(f"Words Result: {words_res}")

        self.stdout.write(self.style.SUCCESS("All requested daily tasks processed."))
