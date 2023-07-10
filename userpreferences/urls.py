from rest_framework import routers
from .views import UserPreferencesViewSet

router = routers.SimpleRouter()
router.register(r'v1', UserPreferencesViewSet, basename='v1')
