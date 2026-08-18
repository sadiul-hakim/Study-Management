from import_export import resources
from .models import WordCollection


class WordCollectionResource(resources.ModelResource):
    class Meta:
        model = WordCollection
        fields = ('id', 'english', 'bengali',
                  'status', 'created_at', 'updated_at')
        export_order = fields
        # avoid duplicate rows on repeated imports of the same word
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True
