from typing import Optional, NamedTuple, Tuple, List

from rest_framework import serializers

from .models import QuizQuestion, QuestionType

from uservocabulary.models import UserVocabularyEntry
from uservocabulary.serializers import UserVocabularyEntrySerializer

from usergrammarrules.models import UserGrammarRuleEntry

from grammarrules.models import GrammarRuleExample
from grammarrules.serializers import GrammarRuleExampleSerializer

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = [ 'id', 'user_vocabulary_entry', 'user_grammar_rule_entry', 'question_type' ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.user_vocabulary_entry is not None:
            display = _convert_user_vocabulary_entry_to_display(
                instance.user_vocabulary_entry,
                instance.question_type,
            )
            response["display"] = DisplaySerializer(display, many=True).data
        elif instance.user_grammar_rule_entry is not None:
            displays, example_id = _convert_user_grammar_rule_to_display(instance.user_grammar_rule_entry, instance.question_type)
            response["display"] = DisplaySerializer(displays, many=True).data
            response["example_id"] = example_id
        else:
            raise ValueError(f"Question {instance.id} has neither an associated grammar rule nor associated vocabulary")
        return response


class Display(NamedTuple):
    display: str
    input_length: int

class DisplaySerializer(serializers.Serializer):
    display = serializers.CharField()
    input_length = serializers.IntegerField(default=1)

def _convert_user_vocabulary_entry_to_display(user_vocabulary_entry: UserVocabularyEntry, question_type: QuestionType) -> List[Display]:
    entry_data = UserVocabularyEntrySerializer(user_vocabulary_entry).data
    word = entry_data["word"]
    if question_type == QuestionType.DefinitionsFromHanzi:
        return [
            Display(
                display=word["display"],
                input_length=1,
            )
        ]
    elif question_type == QuestionType.AccentsFromHanzi:
        return [
            Display(
                display=word["display"],
                input_length=len(word["pronunciation"].split(" ")),
            )
        ]
    elif question_type == QuestionType.HanziFromEnglish:
        return [
            Display(
                display="; ".join([ d["definition"].strip() for d in word["definitions"] if len(d.get("definition", "").strip()) ]),
                input_length=1,
            )
        ]
    else:
        raise ValueError(f"Unrecognized question type {question_type}")

def _convert_user_grammar_rule_to_display(user_grammar_rule: UserGrammarRuleEntry, question_type: QuestionType) -> Tuple[List[Display], str]:
    examples = GrammarRuleExample.objects.filter(
        grammar_rule=user_grammar_rule.grammar_rule, parse_error__isnull=True
    ).order_by("?")
    if not examples:
        raise ValueError(f"Grammar rule {user_grammar_rule.grammar_rule} has no examples")
    example = examples[0]
    serialized = GrammarRuleExampleSerializer(example).data
    if question_type == QuestionType.DefinitionsFromHanzi:
        return [
            Display(
                display=c["word"]["display"],
                input_length=1,
            ) for c in serialized["grammar_rule_example_components"]
        ], example.id
    elif question_type == QuestionType.AccentsFromHanzi:
        return [
            Display(
                display=c["word"]["display"],
                input_length=len(c["word"]["pronunciation"].split(" ")),
            ) for c in serialized["grammar_rule_example_components"]
        ], example.id
    elif question_type == QuestionType.HanziFromEnglish:
        return [
            Display(
                display=example.english_definition,
                input_length=1
            )
        ], example.id
    else:
        raise ValueError(f"Unrecognized question type {question_type}")
