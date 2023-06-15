from rest_framework import serializers

from .models import UserGrammarRuleEntry

class UserGrammarRuleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGrammarRuleEntry
        fields = '__all__'
        read_only_fields = ["user"]