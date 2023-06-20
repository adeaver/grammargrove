from rest_framework import serializers

from .models import UserVocabularyEntry

from words.serializers import WordSerializer

class UserVocabularyEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVocabularyEntry
        fields = '__all__'
        read_only_fields = ["user"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["word"] = WordSerializer(instance.word).data
        return response
