from django.db.models import QuerySet

from users.models import User
from grammarrules.models import GrammarRuleExample, GrammarRuleExamplePrompt
from usergrammarrules.models import UserGrammarRuleEntry
from userpreferences.models import UserPreferences

def get_usable_grammar_rule_examples(user: User) -> QuerySet:
    queryset = GrammarRuleExample.objects.filter(
        parse_error__isnull=True,
        grammar_rule_example_prompt__in=GrammarRuleExamplePrompt.objects.filter(
            is_usable=True
        ),
        grammar_rule__in=UserGrammarRuleEntry.objects.filter(
            user=user
        ).values_list("grammar_rule", flat=True)
    )
    user_preferences = UserPreferences.objects.filter(user=user)
    if user_preferences and user_preferences[0].hsk_level:
       return queryset.filter(max_hsk_level__lte=user_preferences[0].hsk_level)
    return queryset


def get_user_grammar_rules_with_valid_examples(user: User) -> QuerySet:
    usable_grammar_rule_examples = get_usable_grammar_rule_examples(user)
    return UserGrammarRuleEntry.objects.filter(
        user=user,
        grammar_rule__in=usable_grammar_rule_examples.values_list("grammar_rule", flat=True)
    )
