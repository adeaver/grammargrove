from rest_framework import serializers

from .models import QuizQuestion

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = [ 'id', 'user_vocabulary_entry', 'user_grammar_rule_entry', 'question_type' ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.user_vocabulary_entry is not None:
            pass
        elif instance.user_grammar_rule_entry is not None:
            pass
        else:
            raise ValueError(f"Question {instance.id} has neither an associated grammar rule nor associated vocabulary")
        return response


class DisplaySerializer(serializers.Serializer):
    pass
