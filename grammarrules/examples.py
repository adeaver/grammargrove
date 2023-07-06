from typing import Optional, List, Tuple, Optional, NamedTuple
import os
import logging

from django.utils import timezone

import openai

from .models import (
    GrammarRule,
    GrammarRuleComponent,
    GrammarRuleExamplePrompt,
    GrammarRuleExample,
    GrammarRuleExampleComponent,
    GrammarRuleHumanVerifiedPromptExample,
    GrammarRuleHumanVerifiedPromptExampleComponent,
    PartOfSpeech
)
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
    example: Optional[GrammarRuleHumanVerifiedPromptExample] = None
    examples = (
        GrammarRuleHumanVerifiedPromptExample.objects.filter(grammar_rule=grammar_rule).order_by("uses")
    )
    if not examples:
        components = list(GrammarRuleComponent.objects.filter(grammar_rule=grammar_rule).all())
        components.sort(key=lambda x: x.rule_index)
        sentence_structure = "+".join(
            [
                r.word.display if r.word is not None else PartOfSpeech(r.part_of_speech).to_proper_name()
                for r in components
            ]
        )
        prompt = (
            f"Using the sentence structure \"{sentence_structure}\" for {grammar_rule.title}, "
        )
    else:
        example = examples[0]
        example_words = example.hanzi_display.split(" ")
        example_components = (
            GrammarRuleHumanVerifiedPromptExampleComponent.objects.filter(prompt_example=example).order_by("rule_index")
        )
        sentence_structure = "+".join(
            [
                r.word.display if r.word is not None else PartOfSpeech(r.part_of_speech).to_proper_name()
                for r in example_components
            ]
        )
        prompt = (
            f"In Mandarin, the sentence structure {sentence_structure} is used for {example.structure_use}. For example, {example.hanzi_display} {example.explanation}. "
        )
        example.uses += 1
        example.save()
    prompt += (
        f"Create a CSV file with {number_of_examples} in {language}. The CSV file should have the headers "
        f"\"{language} characters,pinyin,English Definition\". Be sure to include all parts of example structure in your answer. "
    )
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
    return list(GrammarRule.objects.order_by("fetch_example_attempts")[:max_number_of_rules])
