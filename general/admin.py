from django.contrib import admin
from .models import Notes, StudyNote

# Register your models here.


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ("book", "page", "note")
    search_fields = ("book", "note",)
    list_filter = ("book",)
    list_per_page = 25


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    search_fields = ("note",)
    change_list_template = "admin/general/note/change_list.html"
    list_per_page = 25

    def has_module_permission(self, request):
        self.model._meta.verbose_name_plural = "Notes"
        return super().has_module_permission(request)
