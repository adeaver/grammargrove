import uuid
from django.db import models

from users.models import User
from grammarrules.models import GrammarRule

class UserGrammarRuleEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grammar_rule = models.ForeignKey(GrammarRule, on_delete=models.CASCADE)
    notes = models.TextField(null=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user', 'grammar_rule'], name='user_grammar_rule_idx')
        ]