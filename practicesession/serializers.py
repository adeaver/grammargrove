from rest_framework import serializers

from .models import PracticeSession

class PracticeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeSession
        fields = '__all__'
        read_only_fields = ["user"]
