from django.db.models import QuerySet

from users.models import User
from grammarrules.query import get_all_valid_grammar_rules
from usergrammarrules.models import UserGrammarRuleEntry
from uservocabulary.models import UserVocabularyEntry
from userpreferences.models import UserPreferences
from words.models import Word, Definition
from ops.featureflags import FeatureFlags

def get_usable_grammar_rule_examples(user: User) -> QuerySet:
    queryset = get_all_valid_grammar_rules(
        use_only_high_quality=FeatureFlags.UseOnlyHighQualityGrammarRuleExamples.flag().get()
    )
    queryset.filter(
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

def get_user_vocabulary_entries_with_valid_definitions(user: User) -> QuerySet:
    valid_words = Word.objects.filter(
        id__in=Definition.objects.filter(
            contains_hanzi=False, is_valid=True
        ).values_list("word", flat=True)
    )
    return UserVocabularyEntry.objects.filter(
        user=user,
        word__in=valid_words,
    )
