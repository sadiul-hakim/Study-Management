from django.contrib import admin
from .models import Book, Chapter, ReadingProgress, Course, ReadingPlan, Revise, OtherStudyProgress

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
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ("book", "chapter", "model", "current_page",
                    "reading_model", "status", "finish_around")
    list_filter = ("book", "status")
    list_per_page = 25


@admin.register(OtherStudyProgress)
class OtherStudyProgressAdmin(admin.ModelAdmin):
    list_display = ("topic_name", "status", "note")
    list_filter = ("status",)
    search_fields = ("topic_name",)
    list_per_page = 25


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_per_page = 25


@admin.register(ReadingPlan)
class ReadingPlanAdmin(admin.ModelAdmin):
    list_display = ("course", "book", "chapter",
                    "start_around", "priority", "order", "note")
    list_filter = ("course", "book", "priority")
    search_fields = ("course__name", "book__title", "note")
    list_per_page = 25


@admin.register(Revise)
class ReviseAdmin(admin.ModelAdmin):
    list_display = ("book", "chapter", "possible_date",
                    "priority",  "order", "note")
    list_filter = ("book", "priority",)
    search_fields = ("book__title", "note")
    list_per_page = 25
