from rest_framework import routers
from .views import OpsViewSet

router = routers.SimpleRouter()
router.register(r'', OpsViewSet, basename='')
