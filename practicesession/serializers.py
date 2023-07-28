from rest_framework import serializers

from .models import PracticeSession, PracticeSessionQuestion
from .mastery import get_mastery_for_session_id

from uservocabulary.serializers import UserVocabularyEntrySerializer
from usergrammarrules.serializers import UserGrammarRuleEntrySerializer

class PracticeSessionQuestionSerializer(serializers.ModelSerializer):
    user_vocabulary_entry = UserVocabularyEntrySerializer()
    user_grammar_rule_entry = UserGrammarRuleEntrySerializer()

    class Meta:
        model = PracticeSessionQuestion
        fields = '__all__'


class PracticeSessionSerializer(serializers.ModelSerializer):
    questions = PracticeSessionQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = PracticeSession
        fields = '__all__'
        read_only_fields = ["user"]


    def to_representation(self, instance):
        response = super().to_representation(instance)
        mastery = get_mastery_for_session_id(instance.user, instance.id)
        response["terms_mastered"] = mastery.terms_mastered
        response["total_number_of_terms"] = mastery.total_number_of_terms
        response["number_of_questions_answered_correctly"] = mastery.number_of_questions_answered_correctly
        response["total_number_of_questions"] = mastery.total_number_of_questions
        return response
