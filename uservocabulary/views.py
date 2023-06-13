from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import UserVocabularyEntry
from .serializers import UserVocabularyEntrySerializer

class UserVocabularyEntryViewSet(viewsets.ModelViewSet):
    serializer_class = UserVocabularyEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserVocabularyEntry.objects.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
