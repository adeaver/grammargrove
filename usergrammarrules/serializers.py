from rest_framework import serializers

from .models import UserGrammarRuleEntry

from grammarrules.serializers import GrammarRuleSerializer

class UserGrammarRuleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGrammarRuleEntry
        fields = '__all__'
        read_only_fields = ["user"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["grammar_rule"] = GrammarRuleSerializer(instance.grammar_rule).data
        return response

