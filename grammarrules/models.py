import uuid
from enum import IntEnum

from django.contrib import admin
from django.db import models
from django.db.models import Q

from words.models import Word, LanguageCode

class GrammarRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_user_added = models.BooleanField(default=False)
    title = models.TextField()
    definition = models.TextField()
    language_code = models.TextField(choices=LanguageCode.choices)
    hsk_level = models.IntegerField()
    fetch_example_attempts = models.IntegerField(default=0)


class GrammarRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "definition", "hsk_level", "components")

    def components(self, obj: GrammarRule):
        components = GrammarRuleComponent.objects.filter(grammar_rule=obj)
        sorted(components, key=lambda x: x.rule_index)
        return " + ".join([
            c.word.display if c.word is not None else c.part_of_speech
            for c in components
        ])

class GrammarRuleComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grammar_rule = models.ForeignKey(GrammarRule, related_name="grammar_rule_components", on_delete=models.CASCADE)
    word = models.ForeignKey(Word, null=True, on_delete=models.CASCADE)
    part_of_speech = models.TextField(null=True)
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


class GrammarRuleHumanVerifiedPromptExampleAdmin(admin.ModelAdmin):
    list_display = ( "grammar_rule", "hanzi_display", "pinyin_display", "structure_use", "explanation", "uses" )


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


class GrammarRuleExampleAdmin(admin.ModelAdmin):
    list_display = ( "id", "grammar_rule", "grammar_rule_example_prompt", "hanzi_display", "pinyin_display", "english_definition", "components", "parse_version", "parse_error")

    def components(self, obj: GrammarRuleExample):
        components = GrammarRuleExampleComponent.objects.filter(grammar_rule_example=obj)
        sorted(components, key=lambda x: x.example_index)
        return "".join([ c.word.display for c in components ])


class GrammarRuleExampleComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grammar_rule_example = models.ForeignKey(GrammarRuleExample, related_name="grammar_rule_example_components", on_delete=models.CASCADE)
    example_index = models.IntegerField()
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['grammar_rule_example', 'example_index'], name='grammar_rule_example_component_index_unique')
        ]
