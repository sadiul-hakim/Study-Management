from import_export import resources
from .models import ReadingProgress, ReadingPlan, Revise


class ReadingProgressResource(resources.ModelResource):
    class Meta:
        model = ReadingProgress
        fields = ("id", "book", "chapter", "model", "current_page",
                  "reading_model", "status", "finish_around")


class ReadingPlanResource(resources.ModelResource):
    class Meta:
        model = ReadingPlan
        fields = ("id", "course", "book", "chapter", "start_around",
                  "priority", "order", "note")


class ReviseResource(resources.ModelResource):
    class Meta:
        model = Revise
        fields = ("id", "book", "chapter", "possible_date",
                  "priority", "order", "note")
