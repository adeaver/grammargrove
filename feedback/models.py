from django.db import models
from django.utils import timezone

from users.models import User

class FeedbackType(models.TextChoices):
    # Asked when someone is joining
    Join = "join", "Join"
    # Asked periodically to see if a user is enjoying it
    Pulse = "pulse", "Pulse"
    # Asked when selecting no thanks on subscription page
    NoSubscribe = "no-sub", "NoSubscribe"

class FeedbackResponse(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response_type = models.TextField(choices=FeedbackType.choices)
    response = models.TextField()
