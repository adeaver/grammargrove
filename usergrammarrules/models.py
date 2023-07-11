import uuid
from django.db import models
from django.utils import timezone

from users.models import User
from grammarrules.models import GrammarRule

class AddedByMethod(models.TextChoices):
    User = "user", "User"
    Onboarding = "onboarding", "Onboarding"

class UserGrammarRuleEntry(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grammar_rule = models.ForeignKey(GrammarRule, related_name="grammar_rule", on_delete=models.CASCADE)
    notes = models.TextField(null=True)
    added_by = models.TextField(choices=AddedByMethod.choices, default=AddedByMethod.User)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user', 'grammar_rule'], name='user_grammar_rule_idx')
        ]
