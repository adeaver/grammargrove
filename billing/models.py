from django.db import models

from django.utils import timezone

from users.models import User

class AccountType(models.TextChoices):
    Stripe = "s", "Stripe"

class Subscription(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.TextField(choices=AccountType.choices)
    user_external_ref = models.TextField(null=True)
    cancel_at = models.DateTimeField(null=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user'], name='billing_subscription_user_idx')
        ]
