import uuid
from enum import IntEnum

from django.db import models
from django.db.models import Q

from words.models import Word, LanguageCode

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
    Place = 17

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    def to_proper_name(self) -> str:
        api_name = self.name
        name_parts = []
        for char in api_name:
            if char.isupper():
                name_parts.append(' ')
            name_parts.append(char.lower())
        return "".join(name_parts).strip()

class GrammarRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_user_added = models.BooleanField(default=False)
    title = models.TextField()
    definition = models.TextField()
    language_code = models.TextField(choices=LanguageCode.choices)
    fetch_example_attempts = models.IntegerField(default=0)

class GrammarRuleComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grammar_rule = models.ForeignKey(GrammarRule, related_name="grammar_rule_components", on_delete=models.CASCADE)
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


class GrammarRuleExampleParseVersion(IntEnum):
    Version1 = 1

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def current_version(cls) -> "GrammarRuleExampleParseVersion":
        return GrammarRuleExampleParseVersion.Version1

# Used for prompting
class GrammarRuleHumanVerifiedPromptExample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grammar_rule = models.ForeignKey(GrammarRule, on_delete=models.CASCADE)
    language_code = models.TextField(choices=LanguageCode.choices)
    hanzi_display = models.TextField()
    pinyin_display = models.TextField()
    structure_use = models.TextField()
    explanation = models.TextField()
    uses = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['grammar_rule'])
        ]

class GrammarRuleHumanVerifiedPromptExampleComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt_example = models.ForeignKey(GrammarRuleHumanVerifiedPromptExample, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, null=True, on_delete=models.CASCADE)
    part_of_speech = models.IntegerField(choices=PartOfSpeech.choices(), null=True)
    rule_index = models.IntegerField()

    class Meta:
        constraints=[
            models.CheckConstraint(
                check=Q(word__isnull=False) | Q(part_of_speech__isnull=False),
                name='human_example_not_both_null'
            ),
            models.UniqueConstraint(fields=['prompt_example', 'rule_index'], name='human_prompt_example_rule_index_unique')
        ]
        indexes = [
            models.Index(fields=['word']),
            models.Index(fields=['part_of_speech']),
        ]



class GrammarRuleExamplePrompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    grammar_rule = models.ForeignKey(GrammarRule, on_delete=models.CASCADE)
    human_verified_example = models.ForeignKey(GrammarRuleHumanVerifiedPromptExample, on_delete=models.CASCADE, null=True)
    prompt = models.TextField()
    response = models.TextField(null=True)
    model = models.TextField()
    usage_tokens = models.IntegerField()
    language_code = models.TextField(choices=LanguageCode.choices)
    parse_version = models.IntegerField(null=True, choices=GrammarRuleExampleParseVersion.choices())

    class Meta:
        indexes = [
            models.Index(fields=['grammar_rule'])
        ]


class GrammarRuleExample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grammar_rule = models.ForeignKey(GrammarRule, on_delete=models.CASCADE)
    grammar_rule_example_prompt = models.ForeignKey(GrammarRuleExamplePrompt, on_delete=models.CASCADE)
    line_idx = models.IntegerField()
    hanzi_display = models.TextField()
    pinyin_display = models.TextField()
    english_definition = models.TextField()
    parse_version = models.IntegerField(null=True, choices=GrammarRuleExampleParseVersion.choices())
    parse_error = models.TextField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['grammar_rule']),
        ]
        constraints=[
            models.UniqueConstraint(fields=['grammar_rule_example_prompt', 'line_idx'], name='grammar_rule_example_line_index_unique'),
            models.UniqueConstraint(fields=['grammar_rule', 'hanzi_display'], name='grammar_rule_display_index_unique')
        ]


class GrammarRuleExampleComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grammar_rule_example = models.ForeignKey(GrammarRuleExample, related_name="grammar_rule_example_components", on_delete=models.CASCADE)
    example_index = models.IntegerField()
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['grammar_rule_example', 'example_index'], name='grammar_rule_example_component_index_unique')
        ]
