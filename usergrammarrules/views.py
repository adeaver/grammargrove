from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from billing.permissions import HasValidSubscription

from .models import UserGrammarRuleEntry
from .serializers import UserGrammarRuleEntrySerializer
from .pagination import UserGrammarRuleEntryPaginator

class UserGrammarRuleEntryViewSet(viewsets.ModelViewSet):
    serializer_class = UserGrammarRuleEntrySerializer
    permission_classes = [IsAuthenticated, HasValidSubscription]
    pagination_class = UserGrammarRuleEntryPaginator

    def get_queryset(self):
        return UserGrammarRuleEntry.objects.filter(user=self.request.user).order_by("-created_at").all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

