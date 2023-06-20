from rest_framework import serializers

import logging

from grammargrove.pinyin_utils import convert_to_display_form

from .models import Word, Definition

class DefintionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = '__all__'

class WordSerializer(serializers.ModelSerializer):
    definitions = DefintionSerializer(many=True, read_only=True)

    class Meta:
        model = Word
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        pronunciation_as_display = " ".join([ convert_to_display_form(p) for p in instance.pronunciation.split(" ")])
        response["pronunciation"] = pronunciation_as_display
        return response
