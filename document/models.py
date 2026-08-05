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


class Document(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Genre")
    )

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def __str__(self):
        return self.name


class DocumentFile(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name=_("Document")
    )

    file = models.FileField(
        _("File"),
        upload_to="documents/"
    )

    class Meta:
        verbose_name = _("Document File")
        verbose_name_plural = _("Document Files")

    def __str__(self):
        return self.file.name


class Link(models.Model):
    name = models.CharField(_("Name"))
    link = models.CharField(_("Link"))
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Genre")
    )

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def __str__(self):
        return self.name
