import uuid

from django.db import models
from django.utils import timezone

from users.models import User
from uservocabulary.models import UserVocabularyEntry
from usergrammarrules.models import UserGrammarRuleEntry
from grammarrules.models import GrammarRuleExample

class PracticeSession(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)


class PracticeSessionQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    practice_session = models.ForeignKey(PracticeSession, related_name="questions", on_delete=models.CASCADE, null=False)
    user_vocabulary_entry = models.ForeignKey(UserVocabularyEntry, on_delete=models.CASCADE, null=True)
    user_grammar_rule_entry = models.ForeignKey(UserGrammarRuleEntry, on_delete=models.CASCADE, null=True)
    grammar_rule_example = models.ForeignKey(GrammarRuleExample, on_delete=models.CASCADE, null=True)
