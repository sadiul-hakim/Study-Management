from django.contrib import admin
from .models import Book, Genre, Author, ReadingProgress, ReadingPlan, StudyNote, Lend
# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre")
    list_filter = ("author", "genre",)
    search_fields = ("title", "author", "genre",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )
    list_per_page = 25


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )
    list_per_page = 25


@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ("book", "reading_page", "is_completed",
                    "is_postponed", "finish_around")
    search_fields = ("book", )
    list_per_page = 25


@admin.register(ReadingPlan)
class ReadingPlanAdmin(admin.ModelAdmin):
    list_display = ("book", "note", "start_around",
                    "order")
    search_fields = ("book", )
    list_per_page = 25


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ("book", "page", "note")
    search_fields = ("book", "note",)
    list_filter = ("book",)
    list_per_page = 25


@admin.register(Lend)
class LendAdmin(admin.ModelAdmin):
    list_display = ("book", "receiver", "date", "return_date")
    search_fields = ("book", "receiver",)
    list_filter = ("receiver",)
    list_per_page = 25
