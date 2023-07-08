import uuid

from django.db import models

class LanguageCode(models.TextChoices):
    SIMPLIFIED_MANDARIN = "ZHCHS", "Simplified"
    TRADITIONAL_MANDARIN = "ZHCHT", "Traditional"
    ENGLISH = "ENG", "English"


class Word(models.Model):
    id = models.TextField(primary_key=True, editable=False)
    language_code = models.TextField(choices=LanguageCode.choices)
    display = models.TextField()
    pronunciation = models.TextField()
    hsk_level = models.IntegerField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['language_code', 'display']),
            models.Index(fields=['language_code', 'pronunciation'])
        ]


class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language_code = models.TextField(choices=LanguageCode.choices)
    word = models.ForeignKey(Word, related_name="definitions", on_delete=models.CASCADE)
    definition = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['word']),
            models.Index(fields=['word', 'language_code'])
        ]
