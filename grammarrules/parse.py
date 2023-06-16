from typing import NamedTuple, List

import csv
import jieba

from grammargrove.pinyin_utils import PinyinSplitter
from .models import (
    GrammarRuleExampleParseVersion,
    GrammarRuleExamplePrompt,
    GrammarRuleExample,
    GrammarRuleExampleComponent,
)
from words.models import Word

class ParseOutput(NamedTuple):
    grammar_rule_examples: List[GrammarRuleExample]
    retryable: bool

def parse_example_prompt(example_prompt_id: str) -> ParseOutput:
    prompts = GrammarRuleExamplePrompt.objects.filter(id=example_prompt_id)
    if not prompts:
        return ParseOutput(grammar_rule_examples=[], retryable=False)
    prompt = prompts[0]
    prompt.parse_version = GrammarRuleExampleParseVersion.current_version()
    splitter = PinyinSplitter()
    reader = csv.reader(prompt.response.split("\n"))
    for idx, row in enumerate(reader):
        if idx == 0:
            continue
        hanzi, pinyin, english_definition = row
        # Step 1: make sure that hanzi and pinyin are the same length
        pinyin_parts = pinyin.split(" ")
        # TODO there's a bug where it returns the whole thing sometimes for some reason
        hanzi_parts = list(jieba.cut(hanzi, cut_all=True))
        if len(pinyin_parts) < len(hanzi_parts):

        elif len(pinyin_parts) > len(hanzi_parts):
            prompt.parse_error = "More pinyin than Hanzi"
            prompt.save()
            return ParseOutput(grammar_rule_examples=[], retryable=False)


