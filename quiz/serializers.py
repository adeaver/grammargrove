from typing import Optional, NamedTuple, Tuple, List

import logging

from rest_framework import serializers

from .models import QuizQuestion, QuestionType
from .utils import get_usable_grammar_rule_examples

from words.models import Word
from words.serializers import WordSerializer
from uservocabulary.models import UserVocabularyEntry
from uservocabulary.serializers import UserVocabularyEntrySerializer

from usergrammarrules.models import UserGrammarRuleEntry
from practicesession.models import PracticeSessionQuestion

from grammarrules.models import GrammarRuleExample
from grammarrules.serializers import GrammarRuleExampleSerializer


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = [ 'id', 'user_vocabulary_entry', 'user_grammar_rule_entry', 'question_type', 'last_displayed_at' ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        practice_session_id: Optional[str] = (
            self.context["request"].GET.get("practice_session_id")
            if "request" in self.context
            else None
        )
        if instance.user_vocabulary_entry is not None:
            display = _convert_user_vocabulary_entry_to_display(
                instance.user_vocabulary_entry,
                instance.question_type,
            )
            response["display"] = DisplaySerializer(display, many=True).data
        elif instance.user_grammar_rule_entry is not None:
            displays, example_id = _convert_user_grammar_rule_to_display(instance.user_grammar_rule_entry, instance.question_type, practice_session_id)
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
                display="; ".join([ d["definition"].strip() for d in word["definitions"] if len(d.get("definition", "").strip()) and not d.get("contains_hanzi", False) ]),
                input_length=1,
            )
        ]
    else:
        raise ValueError(f"Unrecognized question type {question_type}")

def _convert_user_grammar_rule_to_display(
    user_grammar_rule: UserGrammarRuleEntry,
    question_type: QuestionType,
    practice_session_id: Optional[str]
) -> Tuple[List[Display], str]:
    example: Optional[GrammarRuleExample] = None
    if practice_session_id:
        practice_session_question = PracticeSessionQuestion.objects.filter(
            practice_session_id=practice_session_id,
            user_grammar_rule_entry=user_grammar_rule
        ).first()
        example = (
            practice_session_question.grammar_rule_example
            if practice_session_question else None
        )
    if example is None:
        examples_queryset = get_usable_grammar_rule_examples(user_grammar_rule.user)
        examples = examples_queryset.filter(grammar_rule=user_grammar_rule.grammar_rule).order_by("?")
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


class CheckRequestSerializer(serializers.Serializer):
    quiz_question_id = serializers.UUIDField()
    example_id = serializers.UUIDField(allow_null=True)
    answer = serializers.ListField(child=serializers.CharField(required=False, allow_blank=True))
    practice_session_id = serializers.UUIDField(allow_null=True)

class CheckResponse(NamedTuple):
    is_correct: bool
    correct_answer: List[str]
    extra_context: List[str]
    words: List[Word]
    is_practice_session_complete: bool
    terms_mastered: Optional[int]
    total_number_of_terms: Optional[int]
    total_number_of_questions: Optional[int]
    number_of_questions_answered_correctly: Optional[int]


class CheckResponseSerializer(serializers.Serializer):
    is_correct = serializers.BooleanField()
    correct_answer = serializers.ListField(child=serializers.CharField())
    extra_context = serializers.ListField(child=serializers.CharField(required=False, allow_blank=True))
    words = WordSerializer(many=True, required=False)
    is_practice_session_complete = serializers.BooleanField()
    terms_mastered = serializers.IntegerField(required=False)
    total_number_of_terms = serializers.IntegerField(required=False)
    total_number_of_questions = serializers.IntegerField(required=False)
    number_of_questions_answered_correctly = serializers.IntegerField(required=False)



class AddNoteRequestSerializer(serializers.Serializer):
    quiz_question_id = serializers.UUIDField()
    example_id = serializers.UUIDField(allow_null=True)
    note = serializers.CharField()
