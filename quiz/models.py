from typing import List, NamedTuple, Optional

import uuid
from enum import IntEnum

from django.db import models
from django.utils import timezone

from users.models import User
from uservocabulary.models import UserVocabularyEntry
from usergrammarrules.models import UserGrammarRuleEntry
from words.models import Word, Definition, LanguageCode
from grammarrules.models import GrammarRuleExample

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
    user_grammar_rule_entry = models.ForeignKey(UserGrammarRuleEntry, on_delete=models.CASCADE, null=True)
    question_type = models.IntegerField(choices=QuestionType.choices(), null=False)
    number_of_times_displayed = models.IntegerField(null=False, default=0)
    last_displayed_at = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'user_vocabulary_entry', 'question_type'],
                name='question_type_idx',
                condition=models.Q(user_vocabulary_entry__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['user', 'user_grammar_rule_entry', 'question_type'],
                name='grammar_rule_question_type_idx',
                condition=models.Q(user_grammar_rule_entry__isnull=False)
            )
        ]


class QuizResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, null=False)
    is_correct = models.BooleanField(default=False)
    grammar_rule_example = models.ForeignKey(GrammarRuleExample, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
