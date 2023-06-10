from rest_framework import routers
from .views import UserViewSet

router = routers.SimpleRouter()
router.register(r'v1', UserViewSet, basename='v1')
