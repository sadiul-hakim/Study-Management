from django.contrib import admin, messages
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from .models import Improve, Exam

# Register your models here.


@admin.register(Improve)
class ImproveAdmin(admin.ModelAdmin):
    list_display = ("course", "book")
    list_filter = ("course",)
    search_fields = ("course__name", "book__title")
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
            _("Successfully duplicated %(count)d Improve record(s).") % {
                "count": count},
            messages.SUCCESS,
        )



@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "exam_date", "completed")
    list_filter = (
        "course",
        "completed",
        ("exam_date", admin.DateFieldListFilter),
    )
    date_hierarchy = "exam_date"
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
            _("Successfully duplicated %(count)d Exam record(s).") % {
                "count": count},
            messages.SUCCESS,
        )

