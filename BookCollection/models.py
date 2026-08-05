from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Author(models.Model):
    name = models.CharField(_("Name"), max_length=150, unique=True)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name=_("Author")
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        verbose_name=_("Genre")
    )

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title


class ReadingProgress(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    reading_page = models.IntegerField(_("Reading page"), default=0)
    is_completed = models.BooleanField(_("Is completed"), default=False)
    is_postponed = models.BooleanField(_("Is postponed"), default=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    finish_around = models.DateField(_("Finish around"), null=True, blank=True)

    class Meta:
        verbose_name = _("Reading Progress")
        verbose_name_plural = _("Reading Progress")

    def __str__(self):
        return f"{self.book} - page {self.reading_page}"


class ReadingPlan(models.Model):

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    note = models.TextField(_("Note"), blank=True)
    start_around = models.DateField(_("Start around"), null=True, blank=True)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Reading Plan")
        verbose_name_plural = _("Reading Plans")

    def __str__(self):
        return f"{self.book} - {self.book}"


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


class Lend(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    receiver = models.CharField(_("Receiver"), max_length=100)
    date = models.DateField(_("Date"), auto_now=True)
    return_date = models.DateField(_("Return date"), auto_now=True)

    class Meta:
        verbose_name = _("Lend")
        verbose_name_plural = _("Lends")
