from django.db.models import Q, QuerySet

from grammarrules.models import GrammarRuleExample, GrammarRuleExamplePrompt

from ops.featureflags import FeatureFlags

def get_valid_grammar_rule_examples_for_rule(grammar_rule_id: str, use_only_high_quality: bool = False) -> QuerySet:
    queryset = get_all_valid_grammar_rules(use_only_high_quality)
    return queryset.filter(
        grammar_rule_id=grammar_rule_id
    )

def get_all_valid_grammar_rules(use_only_high_quality: bool = False) -> QuerySet:
    examples = GrammarRuleExample.objects.filter(
        parse_error__isnull=True,
        grammar_rule_example_prompt__in=GrammarRuleExamplePrompt.objects.filter(
            is_usable=True,
        ).values_list("id", flat=True)
    )
    if use_only_high_quality:
        return examples.filter(
            validation_score__isnull=False,
            validation_score__gte=FeatureFlags.HighQualityGrammarExampleValidationScoreMin.flag().get()
        )
    return examples
