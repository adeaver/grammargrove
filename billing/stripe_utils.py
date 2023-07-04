from typing import List, Optional

import logging
import stripe

from django.conf import settings

from .serializers import Price

from grammargrove.utils import get_base_url_for_environment
from users.models import User

def get_or_create_customer_from_user(user: User) -> str:
    stripe.api_key = settings.STRIPE_API_KEY
    query = f"email:'{user.email}'"
    resp = stripe.Customer.search(
        query=query
    )
    customer_id: Optional[str] = None
    if not resp.data:
        resp = stripe.Customer.create(email=user.email)
        customer_id = resp.id
    elif resp.has_more or len(resp.data) > 1:
        logging.warn(f"User {user.id} has multiple stripe accounts, randomly choosing the first one")
        customer_id = resp.data[0].id
    else:
        customer_id = resp.data[0].id
    return customer_id


def get_active_prices() -> List[Price]:
    stripe.api_key = settings.STRIPE_API_KEY
    resp = stripe.Price.list(
        active=True,
        product=settings.SUBSCRIPTION_STRIPE_PRODUCT_ID
    )
    out: List[Price] = []
    for price in resp.data:
        price_cents_usd: int = int(price.unit_amount_decimal)
        interval: str = price.recurring.interval.lower().strip()
        price_per_year_usd: Optional[int] = None
        if interval != "year":
            price_per_year_usd = _get_yearly_price(price_cents_usd, interval)
        out.append(
            Price(
                external_price_ref=price.id,
                price_cents_usd=price_cents_usd,
                interval=interval,
                price_per_year_usd=price_per_year_usd,
            )
        )
    sorted(
        out,
        key=lambda x: x.price_per_year_usd if x.price_per_year_usd is not None else x.price_cents_usd
    )
    return out

def _get_yearly_price(
    price_per_interval_cents_usd: int,
    interval: str
) -> int:
    if interval == "month":
        return price_per_interval_cents_usd * 12
    elif interval == "week":
        return price_per_interval_cents_usd * 52
    elif interval == "day":
        return price_per_interval_cents_usd * 365
    else:
        raise ValueError(f"Unrecognized stripe interval {interval}")


def get_checkout_session_url(user: User, price_id: str) -> str:
    stripe.api_key = settings.STRIPE_API_KEY
    customer_id = get_or_create_customer_from_user(user)
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="subscription",
        customer=customer_id,
        success_url=f"{get_base_url_for_environment()}/subscription/?result=success",
        cancel_url=f"{get_base_url_for_environment()}/subscription/?result=cancel",
    )
    return session.url


def get_active_subscription_end_date_for_user(user: User) -> Optional[int]:
    stripe.api_key = settings.STRIPE_API_KEY
    customer_id = get_or_create_customer_from_user(user)
    subs = stripe.Subscription.list(
        customer=customer_id, status="active"
    )
    if not subs.data:
        return None
    elif len(subs.data) > 1:
        logging.warn(f"User {user.id} has multiple active subscriptions, randomly choosing the first one")
    sub = subs.data[0]
    return sub.current_period_end
