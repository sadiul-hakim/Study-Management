from import_export import resources
from .models import WritingPlan


class WritingPlanResource(resources.ModelResource):
    class Meta:
        model = WritingPlan
        fields = ("id", "book", "chapter", "possible_date", "priority", "note")
