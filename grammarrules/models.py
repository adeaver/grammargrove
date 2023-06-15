import uuid
from enum import IntEnum

from django.db import models
from django.db.models import Q

from words.models import Word

class PartOfSpeech(IntEnum):
    Noun = 1
    Pronoun = 2
    Verb = 3
    Adjective = 4
    Adverb = 5
    NumberWord = 6
    Interjection = 7
    Onomatopoeia = 8
    FunctionWord = 9
    Conjunction = 10
    MeasureWord = 11
    Preposition = 12
    Particle = 13
    Predicate = 14
    Subject = 15
    Object = 16

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class GrammarRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_user_added = models.BooleanField(default=False)
    title = models.TextField()
    definition = models.TextField()

class GrammarRuleComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grammar_rule = models.ForeignKey(GrammarRule, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, null=True, on_delete=models.CASCADE)
    part_of_speech = models.IntegerField(choices=PartOfSpeech.choices(), null=True)
    rule_index = models.IntegerField()
    optional = models.BooleanField(default=False)

    class Meta:
        constraints=[
            models.CheckConstraint(
                check=Q(word__isnull=False) | Q(part_of_speech__isnull=False),
                name='not_both_null'
            ),
            models.UniqueConstraint(fields=['grammar_rule', 'rule_index'], name='grammar_rule_index_unique')
        ]
        indexes = [
            models.Index(fields=['word']),
            models.Index(fields=['part_of_speech']),
        ]
