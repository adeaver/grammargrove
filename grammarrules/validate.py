from typing import List, Optional, NamedTuple, Tuple

from django.conf import settings

import deepl
from semantic_text_similarity.models import WebBertSimilarity

from .models import GrammarRuleExample


class TranslationResult(NamedTuple):
    translation: str
    similarity_score: int

class ValidationResults(NamedTuple):
    grammar_rule_id: str
    best_translation: TranslationResult
    translation_contained_in_reverse: Optional[bool]


def validate_grammar_rule_examples(example_ids: List[str]) -> None:
    validation_results = _run_grammar_rule_validation(example_ids)
    for r in validation_results:
        grammar_rule = GrammarRuleExample.objects.filter(
            id=r.grammar_rule_id
        ).first()
        if not grammar_rule:
            continue
        grammar_rule.validation_score = r.best_translation.similarity_score
        grammar_rule.validation_result = r.best_translation.translation
        grammar_rule.save()


def _run_grammar_rule_validation(example_ids: List[str]) -> List[ValidationResults]:
    similarity_model = WebBertSimilarity(device='cpu', batch_size=10)
    translator = deepl.Translator(settings.DEEPL_API_KEY)
    grammar_rule_examples = list(
        GrammarRuleExample.objects.filter(
            parse_error__isnull=True,
            id__in=example_ids
        )
    )
    if not grammar_rule_examples:
        return []
    similarity_requests: List[Tuple[str, str]] = []
    for example in grammar_rule_examples:
        result = translator.translate_text(example.hanzi_display, target_lang="EN-US", source_lang="ZH")
        similarity_requests.append((example.english_definition, result.text))
    similarity_results = similarity_model.predict(similarity_requests)
    return [
        ValidationResults(
            grammar_rule_id=example.id,
            best_translation=TranslationResult(
                similarity_score=int(similarity_results[idx] * 100),
                translation=similarity_requests[idx][1],
            ),
            translation_contained_in_reverse=None
        )
        for idx, example in enumerate(grammar_rule_examples)
    ]


def get_grammar_rules_to_validate(limit: int = 10) -> List[str]:
    return [
        str(example_id)
        for example_id in GrammarRuleExample.objects.filter(
            parse_version__isnull=False,
            parse_error__isnull=True,
            validation_score__isnull=True
        )[:limit].values_list("id", flat=True)
    ]
