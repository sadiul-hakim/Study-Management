from django.contrib import admin
from .models import Improve, Exam

# Register your models here.


@admin.register(Improve)
class ImproveAdmin(admin.ModelAdmin):
    list_display = ("course", "book")
    list_filter = ("course",)
    search_fields = ("course__name", "book__title")
    list_per_page = 25


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "exam_date")
    list_filter = ("course",)
    list_per_page = 25
