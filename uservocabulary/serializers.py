from rest_framework import serializers

from .models import UserVocabularyEntry

class UserVocabularyEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVocabularyEntry
        fields = '__all__'
        read_only_fields = ["user"]
