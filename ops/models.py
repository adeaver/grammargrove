import uuid
from enum import Enum

from django.contrib import admin
from django.db import models
from django.utils import timezone

from datetime import timedelta

VALID_PING_TIME_SECONDS = 60 * 15 # 15 minutes

# This model is created via spooler and checked via /-/healthcheck
class Ping(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    def is_ok(self) -> bool:
        return timezone.now() <= (self.created_at + timedelta(seconds=VALID_PING_TIME_SECONDS))


class FeatureFlagType(Enum):
    Boolean = 'boolean'

class FeatureFlagName(models.TextChoices):
    GrammarRuleFetchesEnabled = "grammar_rule_fetches_enabled", "grammar_rule_fetches_enabled"
    PracticeReminderEmailsEnabled = "practice_reminder_emails_enabled", "practice_reminder_emails_enabled"
    RecaptchaEnabled = "recaptcha_enabled", "recaptcha_enabled"
    GrammarRuleScavengerEnabled = "grammar_rule_scavenger_enabled", "grammar_rule_scavenger_enabled"
    GrammarRuleValidationEnabled = "grammar_rule_validation_enabled", "grammar_rule_validation_enabled"
    UseOnlyHighQualityGrammarRuleExamples = "use_only_high_quality_grammar_rules_examples_enabled", "use_only_high_quality_grammar_rules_examples_enabled"

    def get_type(self) -> FeatureFlagType:
        if self == FeatureFlagName.GrammarRuleFetchesEnabled:
            return FeatureFlagType.Boolean
        elif self == FeatureFlagName.PracticeReminderEmailsEnabled:
            return FeatureFlagType.Boolean
        elif self == FeatureFlagName.RecaptchaEnabled:
            return FeatureFlagType.Boolean
        elif self == FeatureFlagName.GrammarRuleScavengerEnabled:
            return FeatureFlagType.Boolean
        elif self == FeatureFlagName.GrammarRuleValidationEnabled:
            return FeatureFlagType.Boolean
        elif self == FeatureFlagName.UseOnlyHighQualityGrammarRuleExamples:
            return FeatureFlagType.Boolean
        else:
            raise ValueError(f"{self} does not have a type")


class FeatureFlag(models.Model):
    id = models.TextField(primary_key=True, editable=False, choices=FeatureFlagName.choices)
    enabled = models.BooleanField(null=True)


class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ("id", "enabled")
