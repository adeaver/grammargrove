from rest_framework import serializers

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
