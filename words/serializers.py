from typing import Optional
import logging

from rest_framework import serializers

from grammargrove.pinyin_utils import convert_to_display_form

from .models import Word, Definition
from uservocabulary.models import UserVocabularyEntry

class DefintionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = '__all__'

class WordSerializer(serializers.ModelSerializer):
    definitions = DefintionSerializer(many=True, read_only=True)
    user_vocabulary_entry: Optional[str] = None

    class Meta:
        model = Word
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        pronunciation_as_display = " ".join([ convert_to_display_form(p) for p in instance.pronunciation.split(" ")])
        response["pronunciation"] = pronunciation_as_display
        response["definitions"] = [ d for d in response["definitions"] if not d.get("contains_hanzi", False) and d.get("is_valid", False) ]
        user_vocabulary_entry: Optional[str] = None
        if "request" in self.context:
            user = self.context["request"].user
            if user:
                entries = UserVocabularyEntry.objects.filter(user=user, word=instance.id)
                if entries:
                    user_vocabulary_entry = entries[0].id
        response["user_vocabulary_entry"] = user_vocabulary_entry
        return response
