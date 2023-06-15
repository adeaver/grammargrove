from rest_framework import serializers

from .models import GrammarRule, GrammarRuleComponent

class GrammarRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarRule
        fields = '__all__'


class GrammarRuleComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarRuleComponent
        fields = '__all__'
