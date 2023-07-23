import uuid

from django.db import models
from django.utils import timezone

from datetime import timedelta

VALID_PING_TIME_SECONDS = 60 * 15 # 15 minutes

# This model is created via spooler and checked via /-/healthcheck
class Ping(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    def is_ok(self) -> bool:
        return timezone.now() <= (self.created_at + timedelta(seconds=VALID_PING_TIME_SECONDS))
