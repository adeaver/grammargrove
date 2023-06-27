from typing import Optional

from rest_framework import serializers

from .models import (
    GrammarRule,
    GrammarRuleComponent,
    GrammarRuleExample,
    GrammarRuleExampleComponent
)

from words.serializers import WordSerializer
from usergrammarrules.models import UserGrammarRuleEntry


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
    user_grammar_rule_entry: Optional[str] = None

    class Meta:
        model = GrammarRule
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["grammar_rule_components"] = sorted(response["grammar_rule_components"], key=lambda x: x["rule_index"])
        user_grammar_rule_entry: Optional[str] = None
        if "request" in self.context:
            user = self.context["request"].user
            if user:
                entries = UserGrammarRuleEntry.objects.filter(user=user, grammar_rule=instance.id)
                if entries:
                    user_grammar_rule_entry = entries[0].id
        response["user_grammar_rule_entry"] = user_grammar_rule_entry
        return response

class GrammarRuleExampleComponentSerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)

    class Meta:
        model = GrammarRuleExampleComponent
        fields = '__all__'

class GrammarRuleExampleSerializer(serializers.ModelSerializer):
    grammar_rule_example_components = GrammarRuleExampleComponentSerializer(many=True, read_only=True)

    class Meta:
        model = GrammarRuleExample
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["grammar_rule_example_components"] = sorted(response["grammar_rule_example_components"], key=lambda x: x["example_index"])
        return response
