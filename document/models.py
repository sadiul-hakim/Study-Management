from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.


class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        permissions = [
            ("access_genre", "Can access this genre"),
        ]

    def __str__(self):
        return self.name


class GenreAccess(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="access_rules",
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="genre_access_rules",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["genre", "group"],
                name="unique_genre_group_access",
            )
        ]

    def __str__(self):
        return f"{self.group} → {self.genre}"


class Document(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(
        _("Description"), blank=True, max_length=600)
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
    name = models.CharField(_("Name"), max_length=250)
    link = models.CharField(_("Link"), max_length=1000)
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


@receiver(post_delete, sender=DocumentFile)
def delete_file_on_delete(sender, instance, **kwargs):
    """Remove the physical file from storage when a DocumentFile row is deleted."""
    if instance.file:
        instance.file.delete(save=False)
