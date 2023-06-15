from rest_framework import serializers

from .models import GrammarRule, GrammarRuleComponent
from words.serializers import WordSerializer

class GrammarRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarRule
        fields = '__all__'


class GrammarRuleComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarRuleComponent
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['word'] = WordSerializer(instance.word).data
        return response
