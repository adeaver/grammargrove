from typing import Optional, List, Tuple, Optional, NamedTuple
import os
import logging
import random
from uuid import UUID

from django.db.models import Count
from django.utils import timezone

import openai

from .models import (
    GrammarRule,
    GrammarRuleComponent,
    GrammarRuleExamplePrompt,
    GrammarRuleExample,
    GrammarRuleExampleComponent,
    GrammarRuleHumanVerifiedPromptExample,
)
from .utils import ensure_normalized_hanzi
from words.models import LanguageCode

openai.key = os.environ.get("OPENAI_API_KEY", "")
daily_usage_limit = 16

highest_price_by_model = {
    'gpt-3.5-turbo': 0.002,
    'gpt-4': 0.06,
}

def _get_daily_usage() -> float:
    one_day_ago = timezone.now() - timezone.timedelta(days=1)
    example_prompts = GrammarRuleExamplePrompt.objects.filter(created_at__gt=one_day_ago)
    total_usage = 0
    for p in example_prompts:
        total_usage += (p.usage_tokens/1000.0) * highest_price_by_model[p.model]
    return total_usage

def is_over_daily_usage_limit() -> bool:
    return _get_daily_usage() > daily_usage_limit

def fetch_grammar_rule_examples(
    grammar_rule_id: str,
    valid_hsk_levels: Optional[List[int]] = None,
    must_include_words: Optional[List[str]] = None,
    number_of_examples: int = 10,
    language_code: LanguageCode = LanguageCode.SIMPLIFIED_MANDARIN,
    model: str = "gpt-3.5-turbo"
) -> str:
    grammar_rules = GrammarRule.objects.filter(id=grammar_rule_id).all()
    assert len(grammar_rules) == 1
    grammar_rule = grammar_rules[0]
    assert model in highest_price_by_model
    language = "Simplified Mandarin" if language_code == LanguageCode.SIMPLIFIED_MANDARIN else "Traditional Mandarin"
    prompt, human_example = _make_prompt(grammar_rule, valid_hsk_levels, must_include_words, number_of_examples, language_code)
    logging.warn(prompt)
    prompt_record = GrammarRuleExamplePrompt(
        grammar_rule=grammar_rule,
        prompt=prompt,
        human_verified_example=human_example,
        model=model,
        usage_tokens=0,
        language_code=language_code,
    )
    prompt_record.save()
    grammar_rule.fetch_example_attempts += 1
    grammar_rule.save()
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    usage_tokens = openai_response.usage.total_tokens
    message = openai_response.choices[0].message.content
    prompt_record.response = message
    prompt_record.usage_tokens = usage_tokens
    prompt_record.save()
    return prompt_record.id


def _make_prompt(
    grammar_rule: GrammarRule,
    valid_hsk_levels: Optional[List[int]] = None,
    must_include_words: Optional[List[str]] = None,
    number_of_examples: int = 10,
    language_code: LanguageCode = LanguageCode.SIMPLIFIED_MANDARIN,
) -> Tuple[str, Optional[GrammarRuleHumanVerifiedPromptExample]]:
    language = "Simplified Mandarin" if language_code == LanguageCode.SIMPLIFIED_MANDARIN else "Traditional Mandarin"
    prompt: str = ""
    components = list(GrammarRuleComponent.objects.filter(grammar_rule=grammar_rule).all())
    components.sort(key=lambda x: x.rule_index)
    sentence_structure = " + ".join(
        [
            r.word.display if r.word is not None else r.part_of_speech.title()
            for r in components
        ]
    )
    example: Optional[GrammarRuleHumanVerifiedPromptExample] = None
    examples = (
        GrammarRuleHumanVerifiedPromptExample.objects.filter(grammar_rule=grammar_rule).order_by("uses")
    )
    if not examples:
        prompt = (
            f"Using the sentence structure \"{sentence_structure}\" for {grammar_rule.title}, "
        )
    else:
        example = examples[0]
        hanzi_display = ensure_normalized_hanzi("".join(example.hanzi_display.split(" ")))
        prompt = (
            f"In Mandarin, the sentence structure \"{sentence_structure}\" is {example.structure_use}. For example, \"{hanzi_display}\" means \"{example.explanation.lower()}\" \n"
        )
        example.uses += 1
        example.save()
    prompt += (
        f"Create a CSV file with {number_of_examples} in {language}. The CSV file should have the headers "
        f"\"{language} characters,pinyin,English Definition\". Be sure to include all parts of example structure in your answer and make sure that each line in the CSV file that you respond with is a complete sentence. "
    )
    if example:
        hanzi_display = ensure_normalized_hanzi("".join(example.hanzi_display.split(" ")))
        prompt += f"For example, the first line after the header might be: \"{hanzi_display}\",\"{example.pinyin_display}\",\"{example.explanation.lower()}\" "
    if valid_hsk_levels:
        vocabulary_levels = ", ".join([ f"HSK{level}" for level in valid_hsk_levels ])
        prompt += f" Use only vocabulary from {vocabulary_levels}."
    if must_include_words:
        words = ", ".join(must_include_words)
        prompt += f" Make sure the examples include the words: {words}"
    return (prompt, example)


def get_best_candidate_grammar_rules_for_examples(
    max_number_of_rules: int = 5
) -> List[GrammarRule]:
    unused_grammar_rules = GrammarRule.objects.exclude(
        id__in=GrammarRuleExample.objects.filter(
            parse_error__isnull=True,
            parse_version__isnull=False
        ).values_list("grammar_rule_id", flat=True)
    ).order_by("fetch_example_attempts")
    if unused_grammar_rules:
        return unused_grammar_rules[:max_number_of_rules]
    ordered_grammar_rules = (
        GrammarRuleExample.objects.filter(
            parse_error__isnull=True,
            parse_version__isnull=False
        ).values_list("grammar_rule")
         .annotate(dcount=Count("grammar_rule"))
         .order_by("dcount")
    )
    return ordered_grammar_rules[:max_number_of_rules]


def get_best_target_hsk_level_for_grammar_rule(
    grammar_rule_id: str
) -> List[int]:
    current_hsk_levels_with_counts = {
        hsk_level: count
        for hsk_level, count in list(
            GrammarRuleExample.objects.filter(
                grammar_rule_id=grammar_rule_id,
                parse_error__isnull=True,
                parse_version__isnull=False
            )
            .values_list("max_hsk_level")
            .annotate(dcount=Count("max_hsk_level"))
        )
    }
    valid_hsk_levels = [1, 2, 3, 4, 5, 6]
    random.shuffle(valid_hsk_levels)
    sorted(valid_hsk_levels, key=lambda x: current_hsk_levels_with_counts.get(x, 0))
    hsk_level = valid_hsk_levels[0]
    next_hsk_level = 5 if hsk_level == 6 else hsk_level + 1
    return [ hsk_level, next_hsk_level ]

