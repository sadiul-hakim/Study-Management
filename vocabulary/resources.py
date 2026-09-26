from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import WordCollection, VocabularyType


class SmartVocabularyTypeWidget(ForeignKeyWidget):
    """
    Flexible widget that resolves VocabularyType by:
    1. Numeric ID (e.g. 1, 2)
    2. Exact or case-insensitive Name (e.g. "Phrasal Verb", "idiom")
    3. Auto-creates new type if a string name is provided and doesn't exist
    4. Returns None safely if blank or invalid ID (never crashes the import)
    """
    def clean(self, value, row=None, **kwargs):
        if value is None:
            return None
        val_str = str(value).strip()
        if not val_str or val_str.lower() in ['none', 'null', 'nan', '']:
            return None

        # 1. If it's a numeric ID, search by ID
        if val_str.isdigit():
            obj = self.model.objects.filter(id=int(val_str)).first()
            if obj:
                return obj

        # 2. Search by Name (case-insensitive)
        obj = self.model.objects.filter(name__iexact=val_str).first()
        if obj:
            return obj

        # 3. If it's a new name (and not a non-existent integer ID), auto-create
        if not val_str.isdigit():
            obj, _ = self.model.objects.get_or_create(name=val_str)
            return obj

        return None

    def render(self, value, obj=None):
        if value is None:
            return ""
        return getattr(value, 'name', str(value))


class VocabularyTypeResource(resources.ModelResource):
    class Meta:
        model = VocabularyType
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        export_order = fields
        import_id_fields = ('name',)
        skip_unchanged = True
        report_skipped = True


class WordCollectionResource(resources.ModelResource):
    vocabulary_type = fields.Field(
        column_name='vocabulary_type',
        attribute='vocabulary_type',
        widget=SmartVocabularyTypeWidget(VocabularyType, field='name')
    )

    class Meta:
        model = WordCollection
        fields = ('id', 'english', 'bengali', 'vocabulary_type', 'status', 'created_at', 'updated_at')
        export_order = fields
        import_id_fields = ('english',)
        skip_unchanged = True
        report_skipped = True
