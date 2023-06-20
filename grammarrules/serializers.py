from rest_framework import serializers

from .models import GrammarRule, GrammarRuleComponent
from words.serializers import WordSerializer


class GrammarRuleComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarRuleComponent
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.word is not None:
            response['word'] = WordSerializer(instance.word).data
        return response

class GrammarRuleSerializer(serializers.ModelSerializer):
    grammar_rule_components = GrammarRuleComponentSerializer(many=True, read_only=True)

    class Meta:
        model = GrammarRule
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["grammar_rule_components"] = sorted(response["grammar_rule_components"], key=lambda x: x["rule_index"])
        return response
