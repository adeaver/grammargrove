import uuid
from enum import IntEnum

from django.db import models
from django.utils import timezone

from users.models import User
from uservocabulary.models import UserVocabularyEntry

class QuestionType(IntEnum):
    AccentsFromHanzi = 1
    DefinitionsFromHanzi = 2
    HanziFromEnglish = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class QuizQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    user_vocabulary_entry = models.ForeignKey(UserVocabularyEntry, on_delete=models.CASCADE, null=True)
    question_type = models.IntegerField(choices=QuestionType.choices(), null=False)
    number_of_times_displayed = models.IntegerField(null=False, default=1)
    number_of_times_answered_correctly = models.IntegerField(null=False, default=0)
    last_displayed_at = models.DateTimeField(null=False, default=timezone.now)
    last_answered_correctly_at = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'user_vocabulary_entry', 'question_type'],
                name='question_type_idx',
                condition=models.Q(user_vocabulary_entry__isnull=False)
            )
        ]
