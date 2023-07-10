import uuid
from django.db import models

from users.models import User

class UserPreferences(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hsk_level = models.IntegerField(null=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user'], name='user_preferences_users_idx')
        ]
