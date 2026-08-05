from django.urls import path
from .admin_views import document_viewer
from django.contrib import admin
from .models import Document, DocumentFile, Genre, Link
from django.utils.html import format_html
# Register your models here.


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("name", "genre", "link")
    search_fields = ("name", )
    list_filter = ("genre", )
    list_per_page = 25


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )
    list_per_page = 25


class DocumentFileInline(admin.TabularInline):
    model = DocumentFile
    readonly_fields = ("download_link",)
    fields = ("file", "download_link")
    list_per_page = 25

    def download_link(self, obj):
        if obj.pk and obj.file:
            return format_html(
                '<a href="{}" target="_blank">Open</a>',
                obj.file.url
            )
        return "-"


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "genre")
    search_fields = ("name",)
    list_filter = ("genre",)
    list_per_page = 25
    inlines = [DocumentFileInline]

# ---- Viewer


old_get_urls = admin.site.get_urls


def get_urls():
    urls = old_get_urls()

    custom = [
        path(
            "viewer/",
            admin.site.admin_view(document_viewer),
            name="document-viewer",
        ),
    ]

    return custom + urls


admin.site.get_urls = get_urls
