from import_export import resources
from .models import WordCollection


class WordCollectionResource(resources.ModelResource):
    class Meta:
        model = WordCollection
        fields = ('id', 'english', 'bengali', 'status', 'created_at', 'updated_at')
        export_order = fields
        import_id_fields = ('english',)
        skip_unchanged = True
        report_skipped = True
