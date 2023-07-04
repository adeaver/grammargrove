from rest_framework import routers
from .views import FeedbackViewset

router = routers.SimpleRouter()
router.register(r'v1', FeedbackViewset, basename='v1')
