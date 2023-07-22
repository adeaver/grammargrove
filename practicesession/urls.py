from rest_framework import routers
from .views import PracticeSessionViewSet

router = routers.SimpleRouter()
router.register(r'v1', PracticeSessionViewSet, basename='v1')
