from django.contrib import admin, messages
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from .models import WritingPlan
from .resources import WritingPlanResource
# Register your models here.


@admin.register(WritingPlan)
class WritingPlanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = WritingPlanResource
    list_display = ("book", "chapter", "possible_date", "priority", "note")
    list_filter = ("book", "priority",)
    search_fields = ("book__title", "note")
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
            _("Successfully duplicated %(count)d Writing Plan(s).") % {"count": count},
            messages.SUCCESS,
        )
