from rest_framework import routers
from .views import UserGrammarRuleEntryViewSet

router = routers.SimpleRouter()
router.register(r'v1', UserGrammarRuleEntryViewSet, basename='v1')
