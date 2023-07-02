from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Subscription, AccountType
from .permissions import is_user_subscription_status_valid
from .stripe_utils import get_or_create_customer_from_user, get_active_prices
from .serializers import SubscriptionStatusSerializer, SubscriptionStatus

from django.http import HttpRequest

class SubscriptionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def status(self, request: HttpRequest) -> Response:
        if is_user_subscription_status_valid(request.user):
            pass
        subs = Subscription.objects.filter(user=request.user)
        if not subs:
            customer_id = get_or_create_customer_from_user(request.user)
            sub = Subscription(
                user=request.user,
                account_type=AccountType.Stripe,
                user_external_ref=customer_id,
            )
            sub.save()
        else:
            sub = subs[0]
        available_plans = get_active_prices()
        status = SubscriptionStatus(available_plans=available_plans)
        return Response(SubscriptionStatusSerializer(status).data)
