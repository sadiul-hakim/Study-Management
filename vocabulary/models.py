from django.db import models
from django.utils.translation import gettext_lazy as _


class WordCollection(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', _('New')
        FAMILIAR = 'familiar', _('Familiar')
        UNFAMILIAR = 'unfamiliar', _('Unfamiliar')
        CONFIDENT = 'confident', _('Confident')

    english = models.CharField(_('English Word'), max_length=255, unique=True)
    bengali = models.CharField(
        _('Bengali Meaning'), max_length=255, blank=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        db_table = 'general_wordcollection'
        verbose_name = _('Word Collection')
        verbose_name_plural = _('Word Collections')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.english} → {self.bengali}"


class VocabularyExamResult(models.Model):
    class ExamMode(models.TextChoices):
        EN_TO_BN = 'en_to_bn', _('English to Bengali')
        BN_TO_EN = 'bn_to_en', _('Bengali to English')
        MIXED = 'mixed', _('Mixed Practice')

    score = models.IntegerField(_('Score'), default=0)
    total_questions = models.IntegerField(_('Total Questions'), default=10)
    percentage = models.FloatField(_('Percentage'), default=0.0)
    mode = models.CharField(
        _('Mode'),
        max_length=20,
        choices=ExamMode.choices,
        default=ExamMode.EN_TO_BN
    )
    details = models.JSONField(_('Exam Breakdown'), default=dict, blank=True)
    created_at = models.DateTimeField(_('Date Taken'), auto_now_add=True)

    class Meta:
        verbose_name = _('Vocabulary Exam Result')
        verbose_name_plural = _('Vocabulary Exam Results')
        ordering = ['-created_at']

    def __str__(self):
        return f"Exam on {self.created_at.strftime('%Y-%m-%d %H:%M')} — Score: {self.score}/{self.total_questions} ({self.percentage:.1f}%)"


class VerbForm(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', _('New')
        FAMILIAR = 'familiar', _('Familiar')
        UNFAMILIAR = 'unfamiliar', _('Unfamiliar')
        CONFIDENT = 'confident', _('Confident')

    present = models.CharField(_("Base Form"), max_length=100)
    past = models.CharField(_("Past Form"), max_length=100)
    pp = models.CharField(_("Past Participle"), max_length=100, unique=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    def __str__(self):
        return f"{self.present}-{self.past}-{self.pp}"
