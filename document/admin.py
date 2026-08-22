from django.urls import path
from .admin_views import document_viewer
from django.contrib import admin
from .models import Document, DocumentFile, Genre, Link, GenreAccess
from django.utils.html import format_html
from .permissions import get_accessible_documents, get_accessible_links
# Register your models here.


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("name", "genre", "display_link", "open_link")
    search_fields = ("name", "link")
    list_filter = ("genre", )
    list_per_page = 25

    def get_queryset(self, request):
        return get_accessible_links(request.user)

    @admin.display(description="Link")
    def display_link(self, obj):
        if not obj.link:
            return "—"
        truncated = obj.link if len(obj.link) <= 55 else f"{obj.link[:52]}..."
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer" style="color: #4f46e5; text-decoration: underline; word-break: break-all;">{}</a>',
            obj.link,
            truncated
        )

    @admin.display(description="Action")
    def open_link(self, obj):
        if not obj.link:
            return "—"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary" style="padding: 3px 10px; font-size: 12px; white-space: nowrap;">'
            '<i class="fa-solid fa-arrow-up-right-from-square mr-1"></i> Open'
            '</a>',
            obj.link
        )



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )
    list_per_page = 25


@admin.register(GenreAccess)
class GenreAccessAdmin(admin.ModelAdmin):
    list_display = ("genre", "group")
    list_filter = ("genre", "group")
    search_fields = ("genre__name", "group__name")


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

    def get_queryset(self, request):
        return get_accessible_documents(request.user)

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
