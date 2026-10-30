from django.contrib import admin, messages
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from .models import Book, Chapter, Genre, Lend, OtherStudyProgress, StudyNote

# Register your models here.


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "priority")
    list_filter = ("priority",)
    search_fields = ("title",)
    list_per_page = 25

    inlines = [ChapterInline]


@admin.register(OtherStudyProgress)
class OtherStudyProgressAdmin(admin.ModelAdmin):
    list_display = ("topic_name", "book", "chapter", "status", "note")
    list_filter = (
        "status",
        "book",
    )
    list_select_related = (
        "book",
        "chapter",
    )
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
            _("Successfully duplicated %(count)d Other Study Progress record(s).")
            % {"count": count},
            messages.SUCCESS,
        )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 25


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ("book", "page", "note")
    list_select_related = ("book",)
    search_fields = (
        "book",
        "note",
    )
    list_filter = ("book",)
    list_per_page = 25


@admin.register(Lend)
class LendAdmin(admin.ModelAdmin):
    list_display = ("book", "receiver", "date", "return_date")
    list_select_related = ("book",)
    search_fields = (
        "book",
        "receiver",
    )
    list_filter = ("receiver",)
    list_per_page = 25
