from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Book(models.Model):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    PRIORITY_CHOICES = [
        (LOW, _("Low")),
        (MEDIUM, _("Medium")),
        (HIGH, _("High")),
    ]

    genre = models.ForeignKey(
        Genre, on_delete=models.PROTECT, verbose_name=_("Genre"), null=True, blank=True
    )
    title = models.CharField(_("Title"), max_length=255)
    author = models.CharField(_("Author"), max_length=255, blank=True)
    priority = models.IntegerField(
        _("Priority"), choices=PRIORITY_CHOICES, default=MEDIUM
    )

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="chapters", verbose_name=_("Book")
    )
    title = models.CharField(_("Title"), max_length=255)
    chapter_number = models.IntegerField(_("Chapter number"))

    class Meta:
        verbose_name = _("Chapter")
        verbose_name_plural = _("Chapters")

    def __str__(self):
        return f"{self.book.title} - {self.title}"


class OtherStudyProgress(models.Model):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    POSTPONED = 3
    COMPLETED = 4

    PRIORITY_CHOICES = [
        (NOT_STARTED, _("Not Started")),
        (IN_PROGRESS, _("In Progress")),
        (POSTPONED, _("Postponed")),
        (COMPLETED, _("Completed")),
    ]

    topic_name = models.CharField(
        _("Topic name"), max_length=200, null=False, blank=False
    )
    note = models.TextField(
        _("Note"),
        null=True,
        blank=True,
    )
    status = models.IntegerField(
        _("Status"), choices=PRIORITY_CHOICES, default=NOT_STARTED
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="books",
        null=True,
        blank=True,
        verbose_name=_("Book"),
    )

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Chapter"),
    )

    class Meta:
        verbose_name = _("Other Study Progress")
        verbose_name_plural = _("Other Study Progress")

    def __str__(self):
        return f"{self.topic_name}"


class StudyNote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    page = models.IntegerField(_("Page"), default=0)
    note = models.TextField(_("Note"), max_length=500)

    class Meta:
        verbose_name = _("Study Note")
        verbose_name_plural = _("Study Notes")

    def __str__(self):
        return f"{self.book} - Page {self.page}"


class Lend(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    receiver = models.CharField(_("Receiver"), max_length=100)
    date = models.DateField(_("Date"), auto_now=True)
    return_date = models.DateField(_("Return date"), auto_now=True)

    class Meta:
        verbose_name = _("Lend")
        verbose_name_plural = _("Lends")
