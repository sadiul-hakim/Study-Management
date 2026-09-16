from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import WordCollection, VocabularyExamResult, VerbForm
from .resources import WordCollectionResource


@admin.register(WordCollection)
class WordCollectionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [WordCollectionResource]
    list_display = ('english', 'bengali', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('english', 'bengali')
    list_editable = ('status',)
    list_per_page = 50


@admin.register(VerbForm)
class VerbFormAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('present', 'past', 'pp', "status",)
    list_filter = ('status',)
    search_fields = ('present', 'past', 'pp',)
    list_editable = ('status',)
    list_per_page = 50


@admin.register(VocabularyExamResult)
class VocabularyExamResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'score_display', 'mode', 'created_at')
    list_filter = ('mode', 'created_at')
    readonly_fields = ('created_at', 'score', 'total_questions',
                       'percentage', 'mode', 'details')

    def score_display(self, obj):
        return f"{obj.score}/{obj.total_questions} ({obj.percentage:.1f}%)"
    score_display.short_description = "Score"
