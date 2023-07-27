from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from billing.permissions import HasValidSubscription

from .models import UserVocabularyEntry, UserVocabularyNote
from .serializers import UserVocabularyEntrySerializer, UserVocabularyNoteSerializer
from .pagination import UserVocabularyEntryPaginator

class UserVocabularyEntryViewSet(viewsets.ModelViewSet):
    serializer_class = UserVocabularyEntrySerializer
    permission_classes = [IsAuthenticated, HasValidSubscription]
    pagination_class = UserVocabularyEntryPaginator

    def get_queryset(self):
        return UserVocabularyEntry.objects.filter(user=self.request.user).order_by("-created_at").all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
