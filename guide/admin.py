# guides/admin.py

from django.contrib import admin
from .models import Guide


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('priority', 'text')
    ordering = ('priority',)
    list_per_page = 25
