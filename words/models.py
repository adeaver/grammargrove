import uuid
from enum import Enum

from django.db import models

class LanguageCode(Enum):
    SIMPLIFIED_MANDARIN = "ZHCHS"
    TRADITIONAL_MANDARIN = "ZHCHT"
    ENGLISH = "ENG"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Word(models.Model):
    id = models.TextField(primary_key=True, editable=False)
    language_code = models.TextField(choices=LanguageCode.choices())
    display = models.TextField()
    pronunciation = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['language_code', 'display']),
            models.Index(fields=['language_code', 'pronunciation'])
        ]


class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language_code = models.TextField(choices=LanguageCode.choices())
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    definition = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['word']),
            models.Index(fields=['word', 'language_code'])
        ]
