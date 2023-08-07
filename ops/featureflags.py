from typing import Any, List, Generic, TypeVar, Union, Tuple
from enum import Enum

from django.contrib import admin
from django.db import models
from django.db.models import Q

T = TypeVar("T", bound=Union[bool, int])

class _FeatureFlagType(Enum):
    Boolean = ("boolean", bool)
    Integer = ("integer", int)

    def type(self) -> type:
        return self.value[1]

    def name(self) -> str:
        return self.value[0]

    @classmethod
    def choices(cls: Any) -> List[Tuple[str, str]]:
        return [ (_FeatureFlagType(key).name(), _FeatureFlagType(key).name()) for key in cls ]

class _FeatureFlag(Generic[T]):
    def __init__(self, name: str, default: T) -> None:
        self._name = name
        self._default_value = default

    def name(self) -> str:
        return self._name

    def get(self) -> T:
        raise NotImplementedError()

    def initialize(self) -> "FeatureFlag":
        raise NotImplementedError()

    def type(self) -> _FeatureFlagType:
        for flag_type in _FeatureFlagType:
            if isinstance(self._default_value, flag_type.type()):
                return flag_type
        raise NotImplementedError()

class BooleanFeatureFlag(_FeatureFlag[bool]):
    def get(self) -> bool:
        flag = FeatureFlag.objects.filter(id=self.name()).first()
        if not flag:
            return self._default_value
        return flag.enabled

    def initialize(self) -> "FeatureFlag":
        return FeatureFlag(
            id=self.name(),
            flag_type=_FeatureFlagType.Boolean.name(),
            enabled=self._default_value
        )


class IntegerFeatureFlag(_FeatureFlag[int]):
    def get(self) -> int:
        flag = FeatureFlag.objects.filter(id=self.name()).first()
        if not flag:
            return self._default_value
        return flag.int_value

    def initialize(self) -> "FeatureFlag":
        return FeatureFlag(
            id=self.name(),
            flag_type=_FeatureFlagType.Integer.name(),
            int_value=self._default_value
        )


class FeatureFlags(Enum):
    GrammarRuleFetchesEnabled = BooleanFeatureFlag("grammar_rule_fetches_enabled", False)
    PracticeReminderEmailsEnabled = BooleanFeatureFlag("practice_reminder_emails_enabled", False)
    RecaptchaEnabled = BooleanFeatureFlag("recaptcha_enabled", False)
    GrammarRuleScavengerEnabled = BooleanFeatureFlag("grammar_rule_scavenger_enabled", False)
    GrammarRuleValidationEnabled = BooleanFeatureFlag("grammar_rule_validation_enabled", False)
    UseOnlyHighQualityGrammarRuleExamples = BooleanFeatureFlag("use_only_high_quality_grammar_rules_examples_enabled", False)
    NumberOfValidationExamplesPerCycle = IntegerFeatureFlag("number_of_validation_examples_per_cycle", 5)

    def flag(self) -> _FeatureFlag:
        return self.value

    @classmethod
    def get_choices(cls: Any) -> List[Tuple[str, str]]:
        return [ (FeatureFlags(flag).flag().name(), FeatureFlags(flag).flag().name()) for flag in cls ]

    @classmethod
    def initialize(cls: Any) -> None:
        for flag in cls:
            f = FeatureFlags(flag).flag()
            db_flag = FeatureFlag.objects.filter(id=f.name())
            if not db_flag:
                f.initialize().save()

class FeatureFlag(models.Model):
    id = models.TextField(primary_key=True, editable=False, choices=FeatureFlags.get_choices())
    flag_type = models.TextField(choices=_FeatureFlagType.choices(), default=_FeatureFlagType.Boolean.name())
    enabled = models.BooleanField(null=True, blank=True)
    int_value = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(flag_type=_FeatureFlagType.Boolean.name(), enabled__isnull=False, int_value__isnull=True) |
                    Q(flag_type=_FeatureFlagType.Integer.name(), int_value__isnull=False, enabled__isnull=True)
                ),
                name='valid'
            ),
        ]

class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled", "int_value")
