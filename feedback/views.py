from datetime import timedelta

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpRequest
from django.utils import timezone

from .serializers import FeedbackResponseSerializer
from .models import FeedbackResponse, FeedbackType

class FeedbackViewset(viewsets.ModelViewSet):
    serializer_class = FeedbackResponseSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'get']

    def get_queryset(self):
        return FeedbackResponse.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["GET"])
    def check(self, request: HttpRequest) -> Response:
        queryset = self.get_queryset()
        responses = queryset.filter(
            response_type = FeedbackType.Pulse,
            created_at__gt = timezone.now() - timedelta(days=3)
        )
        return Response(self.serializer_class(responses, many=True).data)
