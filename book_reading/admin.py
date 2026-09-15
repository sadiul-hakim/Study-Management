from datetime import timedelta
from django.contrib import admin, messages
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from writing_plan.models import WritingPlan
from .models import Book, Chapter, ReadingProgress, Course, ReadingPlan, Revise, OtherStudyProgress

from .resources import ReadingProgressResource, ReadingPlanResource, ReviseResource
from import_export.admin import ImportExportModelAdmin
# Models


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "priority")
    list_filter = ("priority", "course")
    search_fields = ("title",)
    list_per_page = 25

    inlines = [ChapterInline]


@admin.register(ReadingProgress)
class ReadingProgressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ReadingProgressResource
    list_display = ("book", "chapter", "model", "current_page",
                    "reading_model", "status", "finish_around")
    list_filter = ("book", "status")
    list_per_page = 25
    actions = ["move_to_revise", "move_to_writing_plan", "copy_entry"]

    @admin.action(description=_("Move to Revise"))
    def move_to_revise(self, request, queryset):
        target_date = timezone.localdate() + timedelta(days=5)
        count = 0
        with transaction.atomic():
            for progress in queryset:
                Revise.objects.create(
                    book=progress.book,
                    chapter=progress.chapter,
                    priority=progress.book.priority if progress.book else Revise.MEDIUM,
                    possible_date=target_date,
                    order=0,
                    note="",
                )
                count += 1
            queryset.delete()

        self.message_user(
            request,
            _("Successfully moved %(count)d Reading Progress record(s) to Revise (Scheduled for %(date)s).") % {
                "count": count,
                "date": target_date,
            },
            messages.SUCCESS,
        )

    @admin.action(description=_("Move to Writing Plan"))
    def move_to_writing_plan(self, request, queryset):
        target_date = timezone.localdate() + timedelta(days=5)
        count = 0
        with transaction.atomic():
            for progress in queryset:
                WritingPlan.objects.create(
                    book=progress.book,
                    chapter=progress.chapter,
                    priority=progress.book.priority if progress.book else WritingPlan.MEDIUM,
                    possible_date=target_date,
                    note="",
                )
                count += 1
            queryset.delete()

        self.message_user(
            request,
            _("Successfully moved %(count)d Reading Progress record(s) to Writing Plan (Scheduled for %(date)s).") % {
                "count": count,
                "date": target_date,
            },
            messages.SUCCESS,
        )

    @admin.action(description=_("Copy"))
    def copy_entry(self, request, queryset):
        count = 0
        with transaction.atomic():
            for obj in queryset:
                obj.pk = None
                obj.save()
                count += 1

        self.message_user(
            request,
            _("Successfully duplicated %(count)d Reading Progress record(s).") % {"count": count},
            messages.SUCCESS,
        )


@admin.register(OtherStudyProgress)
class OtherStudyProgressAdmin(admin.ModelAdmin):
    list_display = ("topic_name", "status", "note")
    list_filter = ("status",)
    search_fields = ("topic_name",)
    list_per_page = 25
    actions = ["copy_entry"]

    @admin.action(description=_("Copy"))
    def copy_entry(self, request, queryset):
        count = 0
        with transaction.atomic():
            for obj in queryset:
                obj.pk = None
                obj.save()
                count += 1

        self.message_user(
            request,
            _("Successfully duplicated %(count)d Other Study Progress record(s).") % {"count": count},
            messages.SUCCESS,
        )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_per_page = 25


@admin.register(ReadingPlan)
class ReadingPlanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ReadingPlanResource
    list_display = ("course", "book", "chapter",
                    "start_around", "priority", "order", "note")
    list_filter = ("course", "book", "priority")
    search_fields = ("course__name", "book__title", "note")
    list_per_page = 25
    actions = ["move_to_revise", "move_to_writing_plan", "copy_entry"]

    @admin.action(description=_("Move to Revise"))
    def move_to_revise(self, request, queryset):
        target_date = timezone.localdate() + timedelta(days=5)
        count = 0
        with transaction.atomic():
            for plan in queryset:
                Revise.objects.create(
                    book=plan.book,
                    chapter=plan.chapter,
                    priority=plan.priority,
                    possible_date=target_date,
                    order=0,
                    note=plan.note or "",
                )
                count += 1
            queryset.delete()

        self.message_user(
            request,
            _("Successfully moved %(count)d Reading Plan(s) to Revise (Scheduled for %(date)s).") % {
                "count": count,
                "date": target_date,
            },
            messages.SUCCESS,
        )

    @admin.action(description=_("Move to Writing Plan"))
    def move_to_writing_plan(self, request, queryset):
        target_date = timezone.localdate() + timedelta(days=5)
        count = 0
        with transaction.atomic():
            for plan in queryset:
                WritingPlan.objects.create(
                    book=plan.book,
                    chapter=plan.chapter,
                    priority=plan.priority,
                    possible_date=target_date,
                    note=plan.note or "",
                )
                count += 1
            queryset.delete()

        self.message_user(
            request,
            _("Successfully moved %(count)d Reading Plan(s) to Writing Plan (Scheduled for %(date)s).") % {
                "count": count,
                "date": target_date,
            },
            messages.SUCCESS,
        )

    @admin.action(description=_("Copy"))
    def copy_entry(self, request, queryset):
        count = 0
        with transaction.atomic():
            for obj in queryset:
                obj.pk = None
                obj.save()
                count += 1

        self.message_user(
            request,
            _("Successfully duplicated %(count)d Reading Plan(s).") % {"count": count},
            messages.SUCCESS,
        )


@admin.register(Revise)
class ReviseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ReviseResource
    list_display = ("book", "chapter", "possible_date",
                    "priority",  "order", "note")
    list_filter = ("book", "priority",)
    search_fields = ("book__title", "note")
    list_per_page = 25
    actions = ["move_to_writing_plan", "copy_entry"]

    @admin.action(description=_("Move to Writing Plan"))
    def move_to_writing_plan(self, request, queryset):
        target_date = timezone.localdate() + timedelta(days=5)
        count = 0
        with transaction.atomic():
            for revise in queryset:
                WritingPlan.objects.create(
                    book=revise.book,
                    chapter=revise.chapter,
                    priority=revise.priority,
                    possible_date=target_date,
                    note=revise.note or "",
                )
                count += 1
            queryset.delete()

        self.message_user(
            request,
            _("Successfully moved %(count)d Revise record(s) to Writing Plan (Scheduled for %(date)s).") % {
                "count": count,
                "date": target_date,
            },
            messages.SUCCESS,
        )

    @admin.action(description=_("Copy"))
    def copy_entry(self, request, queryset):
        count = 0
        with transaction.atomic():
            for obj in queryset:
                obj.pk = None
                obj.save()
                count += 1

        self.message_user(
            request,
            _("Successfully duplicated %(count)d Revise record(s).") % {"count": count},
            messages.SUCCESS,
        )
