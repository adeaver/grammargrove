import uuid
from django.db import models
from django.utils import timezone

from users.models import User
from words.models import Word

class AddedByMethod(models.TextChoices):
    User = "user", "User"
    Onboarding = "onboarding", "Onboarding"

class UserVocabularyEntry(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    added_by = models.TextField(choices=AddedByMethod.choices, default=AddedByMethod.User)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user', 'word'], name='user_word_vocabulary')
        ]


class UserVocabularyNote(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_vocabulary_entry = models.ForeignKey(UserVocabularyEntry, related_name="notes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['user_vocabulary_entry']),
        ]
