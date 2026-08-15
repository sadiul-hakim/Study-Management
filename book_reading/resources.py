from import_export import resources
from .models import ReadingProgress


class ReadingProgressResource(resources.ModelResource):
    class Meta:
        model = ReadingProgress
        fields = ("id", "book", "chapter", "model", "current_page",
                  "reading_model", "status", "finish_around")
