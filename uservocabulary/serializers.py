from rest_framework import serializers

from .models import UserVocabularyEntry, UserVocabularyNote

from words.serializers import WordSerializer


class UserVocabularyNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVocabularyNote
        fields = '__all__'
        read_only_fields = ["user"]

class UserVocabularyEntrySerializer(serializers.ModelSerializer):
    notes = UserVocabularyNoteSerializer(many=True)

    class Meta:
        model = UserVocabularyEntry
        fields = '__all__'
        read_only_fields = ["user"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["word"] = WordSerializer(instance.word).data
        return response
