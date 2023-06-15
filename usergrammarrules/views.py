from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import UserGrammarRuleEntry
from .serializers import UserGrammarRuleEntrySerializer

class UserGrammarRuleEntryViewSet(viewsets.ModelViewSet):
    serializer_class = UserGrammarRuleEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserGrammarRuleEntry.objects.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
