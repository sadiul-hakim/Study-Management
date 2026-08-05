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


class LiteraryWork(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="works",
        verbose_name=_("Author")
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name="works",
        verbose_name=_("Genre")
    )

    class Meta:
        verbose_name = _("Literary Work")
        verbose_name_plural = _("Literary Works")

    def __str__(self):
        return self.name
