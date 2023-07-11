from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from billing.permissions import HasValidSubscription

from .models import UserPreferences
from .serializers import UserPreferencesSerializer

class UserPreferencesViewSet(viewsets.ModelViewSet):
    serializer_class = UserPreferencesSerializer
    permission_classes = [IsAuthenticated, HasValidSubscription]

    def get_queryset(self):
        return UserPreferences.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
