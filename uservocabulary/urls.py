from rest_framework import routers
from .views import UserVocabularyEntryViewSet, UserVocabularyNoteViewSet

router = routers.SimpleRouter()
router.register(r'v1', UserVocabularyEntryViewSet, basename='v1')
router.register(r'notes/v1', UserVocabularyNoteViewSet, basename='v1-notes')
