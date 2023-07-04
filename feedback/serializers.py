from rest_framework import serializers

from .models import FeedbackResponse

class FeedbackResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackResponse
        fields = '__all__'
        read_only_fields = ["user", "created_at"]
