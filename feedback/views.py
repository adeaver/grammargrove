from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import FeedbackResponseSerializer
from .models import FeedbackResponse

class FeedbackViewset(viewsets.ModelViewSet):
    serializer_class = FeedbackResponseSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def get_queryset(self):
        return FeedbackResponse.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
