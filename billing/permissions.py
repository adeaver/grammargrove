from datetime import datetime, timedelta

from django.utils import timezone
from django.http import HttpRequest

from rest_framework import permissions

from .models import Subscription
from .stripe_utils import get_active_subscription_end_date_for_user

from users.models import User

LENGTH_OF_FREE_TRIAL_DAYS = 10
BUFFER_PERIOD_DAYS = 3

def is_user_subscription_status_valid(user: User) -> bool:
    requires_subscription = user.date_joined < (timezone.now() - timedelta(days=LENGTH_OF_FREE_TRIAL_DAYS))
    if not requires_subscription:
        return True
    return _verify_subscription_valid(user)


def _verify_subscription_valid(user: User) -> bool:
    subs = Subscription.objects.filter(user=user)
    if not subs:
        return False
    sub = subs[0]
    if sub.cancel_at is not None and sub.cancel_at > timezone.now():
        return True
    cancel_at_timestamp = get_active_subscription_end_date_for_user(user)
    if cancel_at_timestamp is None:
        return False
    tz_aware_timestamp = timezone.make_aware(datetime.fromtimestamp(cancel_at_timestamp) + timedelta(days=BUFFER_PERIOD_DAYS))
    sub.cancel_at = tz_aware_timestamp
    sub.save()
    return True


class HasValidSubscription(permissions.BasePermission):
    message = "Your subscription is invalid"

    def has_permission(self, request: HttpRequest, view) -> bool:
        return (
            request.user is not None and
            is_user_subscription_status_valid(request.user)
        )
