from django.db import models
from django.utils.translation import gettext_lazy as _
from book_reading.models import Course, Book

# Create your models here.


class Exam(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course"))
    name = models.CharField(_("Name"), max_length=200)
    exam_date = models.DateField(_("Exam date"))

    class Meta:
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")

    def __str__(self):
        return self.name


class Improve(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course"))
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_("Book"))

    class Meta:
        verbose_name = _("Improve")
        verbose_name_plural = _("Improve")

    def __str__(self):
        return f"{self.course} - {self.book}"
