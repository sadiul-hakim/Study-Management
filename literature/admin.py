from django.contrib import admin

# Register your models here.
from .models import Genre, LiteraryWork, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 25


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 25


@admin.register(LiteraryWork)
class LiteraryWorkAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "genre")
    list_filter = ("genre", "author")
    search_fields = ("name", "author__name")
    list_per_page = 25
