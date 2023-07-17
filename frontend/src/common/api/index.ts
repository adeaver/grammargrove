export type Word = {
    id: string;
    language_code: string;
    display: string;
    pronunciation: string;
    definitions: Array<Definition>;
    user_vocabulary_entry: string | null;
}

export type Definition = {
   id: string;
   language_code: string;
   definition: string;
   word: string;
}

export type GrammarRule = {
    id: string;
    is_user_added: boolean;
    definition: string;
    grammar_rule_components: Array<GrammarRuleComponent>;
    language_code: string;
    user_grammar_rule_entry: string | null;
    hsk_level: number;
}

export type GrammarRuleComponent = {
    id: string;
    grammar_rule: string;
    word: Word | null;
    part_of_speech: string | null;
    rule_index: number;
    optional: boolean;
}
