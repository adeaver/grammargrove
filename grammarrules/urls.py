from rest_framework import routers
from .views import GrammarRuleViewSet

router = routers.SimpleRouter()
router.register(r'v1', GrammarRuleViewSet, basename='v1')
