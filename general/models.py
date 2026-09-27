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
    title = models.CharField(_("Title"), max_length=200, blank=True, default="")
    note = CKEditor5Field(_('Note'), config_name='default')
    order = models.IntegerField(_("Order"), default=0)
    show_on_home_page = models.BooleanField(_("Show on home page"), default=False)

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        ordering = ["order"]

    def __str__(self):
        return self.title if self.title else self.note[:50]


