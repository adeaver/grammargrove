from rest_framework import routers
from .views import QuizViewSet

router = routers.SimpleRouter()
router.register(r'v1', QuizViewSet, basename='v1')
