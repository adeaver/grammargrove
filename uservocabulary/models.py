import uuid
from django.db import models
from django.utils import timezone

from users.models import User
from words.models import Word

class UserVocabularyEntry(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    notes = models.TextField(null=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user', 'word'], name='user_word_vocabulary')
        ]
