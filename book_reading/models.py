from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Course(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

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

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="books", null=True,
        blank=True, verbose_name=_("Course"))
    title = models.CharField(_("Title"), max_length=255)
    author = models.CharField(_("Author"), max_length=255, blank=True)
    priority = models.IntegerField(
        _("Priority"), choices=PRIORITY_CHOICES, default=MEDIUM)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="chapters",
        verbose_name=_("Book")
    )
    title = models.CharField(_("Title"), max_length=255)
    chapter_number = models.IntegerField(_("Chapter number"))

    class Meta:
        verbose_name = _("Chapter")
        verbose_name_plural = _("Chapters")

    def __str__(self):
        return f"{self.book.title} - {self.title}"


class ReadingProgress(models.Model):
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

    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_("Chapter"))
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    current_page = models.IntegerField(_("Current page"), default=0)
    model = models.CharField(_("Model"), max_length=100, default=0)
    status = models.IntegerField(
        _("Status"), choices=PRIORITY_CHOICES, default=NOT_STARTED)
    reading_model = models.BooleanField(_("Reading model"), default=False)

    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    finish_around = models.DateField(_("Finish around"), null=True, blank=True)

    class Meta:
        verbose_name = _("Reading Progress")
        verbose_name_plural = _("Reading Progress")

    def __str__(self):
        return f"{self.chapter} - page {self.current_page}"


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
        _("Topic name"), max_length=200, null=False, blank=False)
    note = models.TextField(_("Note"))
    status = models.IntegerField(
        _("Status"), choices=PRIORITY_CHOICES, default=NOT_STARTED)

    class Meta:
        verbose_name = _("Other Study Progress")
        verbose_name_plural = _("Other Study Progress")

    def __str__(self):
        return f"{self.topic_name}"


class ReadingPlan(models.Model):
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
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course"))
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_("Chapter"))
    note = models.TextField(_("Note"), blank=True)
    start_around = models.DateField(_("Start around"), null=True, blank=True)
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Reading Plan")
        verbose_name_plural = _("Reading Plans")

    def __str__(self):
        return f"{self.course} - {self.book}"


class Revise(models.Model):
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
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Revise")
        verbose_name_plural = _("Revises")

    def __str__(self):
        return f"{self.book} - {self.chapter}"
