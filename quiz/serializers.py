from typing import Optional, NamedTuple

from rest_framework import serializers

from .models import QuizQuestion, QuestionType

from uservocabulary.models import UserVocabularyEntry
from uservocabulary.serializers import UserVocabularyEntrySerializer

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
            response["display"] = DisplaySerializer(display).data
        elif instance.user_grammar_rule_entry is not None:
            pass
        else:
            raise ValueError(f"Question {instance.id} has neither an associated grammar rule nor associated vocabulary")
        return response


class Display(NamedTuple):
    display: str
    input_length: int
    parent_id: Optional[str]

class DisplaySerializer(serializers.Serializer):
    display = serializers.CharField()
    input_length = serializers.IntegerField(default=1)
    parent_id = serializers.UUIDField(allow_null=True)

def _convert_user_vocabulary_entry_to_display(user_vocabulary_entry: UserVocabularyEntry, question_type: QuestionType) -> Display:
    entry_data = UserVocabularyEntrySerializer(user_vocabulary_entry).data
    word = entry_data["word"]
    if question_type == QuestionType.DefinitionsFromHanzi:
        return Display(
            display=word["display"],
            input_length=1,
            parent_id=None,
        )
    elif question_type == QuestionType.AccentsFromHanzi:
        return Display(
            display=word["display"],
            input_length=len(word["pronunciation"].split(" ")),
            parent_id=None,
        )
    elif question_type == QuestionType.HanziFromEnglish:
        return Display(
            display="; ".join([ d["definition"].strip() for d in word["definitions"] if len(d.get("definition", "").strip()) ]),
            input_length=1,
            parent_id=None,
        )
    else:
        raise ValueError(f"Unrecognized question type {question_type}")
