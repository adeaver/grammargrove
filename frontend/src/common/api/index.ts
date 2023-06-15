export enum PartOfSpeech {
    Noun = 1,
    Pronoun = 2,
    Verb = 3,
    Adjective = 4,
    Adverb = 5,
    NumberWord = 6,
    Interjection = 7,
    Onomatopoeia = 8,
    FunctionWord = 9,
    Conjunction = 10,
    MeasureWord = 11,
    Preposition = 12,
    Particle = 13,
    Predicate = 14,
    Subject = 15,
    Object = 16
}

export function partOfSpeechToDisplay(p: PartOfSpeech) {
    switch (p) {
        case PartOfSpeech.Noun:
            return "Noun"
        case PartOfSpeech.Pronoun:
            return "Pronoun"
        case PartOfSpeech.Verb:
            return "Verb"
        case PartOfSpeech.Adjective:
            return "Adjective"
        case PartOfSpeech.Adverb:
            return "Adverb"
        case PartOfSpeech.NumberWord:
            return "Number Word"
        case PartOfSpeech.Interjection:
            return "Interjection"
        case PartOfSpeech.Onomatopoeia:
            return "Onomatopoeia"
        case PartOfSpeech.FunctionWord:
            return "Function Word"
        case PartOfSpeech.Conjunction:
            return "Conjunction"
        case PartOfSpeech.MeasureWord:
            return "Measure Word"
        case PartOfSpeech.Preposition:
            return "Preposition"
        case PartOfSpeech.Particle:
            return "Particle"
        case PartOfSpeech.Predicate:
            return "Predicate"
        case PartOfSpeech.Subject:
            return "Subject"
        case PartOfSpeech.Object:
            return "Object"
        default:
            throw new Error("Unknown part of speech")
    }
}

export type Word = {
    id: string;
    language_code: string;
    display: string;
    pronunciation: string;
}

export type GrammarRule = {
    id: string;
    is_user_added: boolean;
    title: string;
    definition: string;
}

export type GrammarRuleComponent = {
    id: string;
    grammar_rule: string;
    word: Word | null;
    part_of_speech: PartOfSpeech | null;
    rule_index: number;
    optional: boolean;
}
