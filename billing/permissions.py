from datetime import timedelta

from django.utils import timezone
from django.http import HttpRequest

from rest_framework import permissions

from users.models import User

LENGTH_OF_FREE_TRIAL_DAYS = 10

def is_user_subscription_status_valid(user: User) -> bool:
    requires_subscription = user.date_joined < (timezone.now() - timedelta(days=LENGTH_OF_FREE_TRIAL_DAYS))
    if not requires_subscription:
        return True
    # TODO(check subscription status here)
    return False


class HasValidSubscription(permissions.BasePermission):
    message = "Your subscription is invalid"

    def has_permission(self, request: HttpRequest, view) -> bool:
        return (
            request.user is not None and
            is_user_subscription_status_valid(request.user)
        )
