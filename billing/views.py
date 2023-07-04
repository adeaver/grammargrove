from django.shortcuts import redirect
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Subscription, AccountType
from .permissions import is_user_subscription_status_valid
from .stripe_utils import (
    get_or_create_customer_from_user,
    get_active_prices,
    get_checkout_session_url
)
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

    @action(detail=False, methods=["post"])
    def checkout(self, request: HttpRequest) -> Response:
        subs = Subscription.objects.filter(user=request.user)
        if subs:
            sub = subs[0]
            if sub.cancel_at is not None and sub.cancel_at < timezone.now():
                # User already has valid subscription
                # should redirect to manage page?
                return redirect("/subscription/")
        checkout_session = get_checkout_session_url(request.user, request.POST["price_id"])
        return redirect(checkout_session)
