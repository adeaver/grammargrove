from rest_framework import routers
from .views import SubscriptionViewSet

router = routers.SimpleRouter()
router.register(r'v1', SubscriptionViewSet, basename='v1')
