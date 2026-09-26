from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from .models import WordCollection, VocabularyExamResult, VerbForm, VocabularyType
from .resources import WordCollectionResource, VocabularyTypeResource


@admin.register(VocabularyType)
class VocabularyTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [VocabularyTypeResource]
    list_display = ('name', 'description', 'word_count', 'created_at')
    search_fields = ('name', 'description')
    list_per_page = 50

    def word_count(self, obj):
        return obj.words.count()
    word_count.short_description = _("Total Words")


@admin.register(WordCollection)
class WordCollectionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [WordCollectionResource]
    list_display = ('english', 'bengali', 'vocabulary_type', 'status', 'created_at')
    list_filter = ('vocabulary_type', 'status', 'created_at')
    search_fields = ('english', 'bengali')
    list_editable = ('vocabulary_type', 'status')
    list_select_related = ('vocabulary_type',)
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
