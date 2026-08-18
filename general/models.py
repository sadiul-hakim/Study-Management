from django.db import models
from django.utils.translation import gettext_lazy as _
from book_reading.models import Book
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.


class StudyNote(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    page = models.IntegerField(_("Page"), default=0)
    note = models.TextField(_("Note"), max_length=500)

    class Meta:
        verbose_name = _("Study Note")
        verbose_name_plural = _("Study Notes")

    def __str__(self):
        return f"{self.book} - Page {self.page}"


class Notes(models.Model):
    note = CKEditor5Field(_('Note'), config_name='default')

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    def __str__(self):
        return self.note[:50]


class WordCollection(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        FAMILIAR = 'familiar', 'Familiar'
        UNFAMILIAR = 'unfamiliar', 'Unfamiliar'
        CONFIDENT = 'confident', 'Confident'

    english = models.CharField(max_length=255, unique=True)
    bengali = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Word Collection"
        verbose_name_plural = "Word Collections"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.english} → {self.bengali}"
