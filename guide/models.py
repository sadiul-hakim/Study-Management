from django.db import models
from django.utils.translation import gettext_lazy as _


class Guide(models.Model):
    PRIMARY = 1
    WARNING = 2
    DANGER = 3

    TYPE = [
        (PRIMARY, _("Primary")),
        (WARNING, _("Warning")),
        (DANGER, _("Danger")),
    ]

    text = models.TextField(_("Text"))
    priority = models.IntegerField(_("Priority"), default=0)
    type = models.IntegerField(_("Type"), choices=TYPE, default=WARNING)

    class Meta:
        ordering = ['priority']
        verbose_name = _("Guide")
        verbose_name_plural = _("Guides")

    def __str__(self):
        return f"Guide {self.priority}"

    def bootstrap_class(self):
        return {
            self.PRIMARY: "card-primary",
            self.WARNING: "card-warning",
            self.DANGER: "card-danger",
        }.get(self.type, "card-secondary")

    def save(self, *args, **kwargs):
        from django.core.cache import cache
        cache.delete("admin_guide_cached")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        from django.core.cache import cache
        cache.delete("admin_guide_cached")
        super().delete(*args, **kwargs)
