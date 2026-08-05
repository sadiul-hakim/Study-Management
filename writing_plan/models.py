from django.db import models
from django.utils.translation import gettext_lazy as _

from book_reading.models import Book, Chapter

# Create your models here.


class WritingPlan(models.Model):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    PRIORITY_CHOICES = [
        (LOW, _("Low")),
        (MEDIUM, _("Medium")),
        (HIGH, _("High")),
    ]

    priority = models.IntegerField(
        _("Priority"), choices=PRIORITY_CHOICES, default=MEDIUM)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_("Chapter"))
    note = models.TextField(_("Note"), blank=True)
    possible_date = models.DateField(_("Possible date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Writing Plan")
        verbose_name_plural = _("Writing Plans")

    def __str__(self):
        return f"{self.book} - {self.chapter}"
