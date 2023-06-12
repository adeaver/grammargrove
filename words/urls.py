from rest_framework import routers
from .views import WordsViewSet

router = routers.SimpleRouter()
router.register(r'v1', WordsViewSet, basename='v1')
