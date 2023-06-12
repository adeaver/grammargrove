from rest_framework import routers
from .views import UserVocabularyEntryViewSet

router = routers.SimpleRouter()
router.register(r'v1', UserVocabularyEntryViewSet, basename='v1')
