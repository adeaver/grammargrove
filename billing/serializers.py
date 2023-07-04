from typing import List, NamedTuple, Optional

from rest_framework import serializers

class Price(NamedTuple):
    external_price_ref: str
    price_cents_usd: int
    interval: str
    price_per_year_usd: Optional[int]

class PriceSerializer(serializers.Serializer):
    external_price_ref = serializers.CharField()
    price_cents_usd = serializers.IntegerField()
    interval = serializers.CharField()
    price_per_year_usd = serializers.IntegerField(required=False)

class SubscriptionStatus(NamedTuple):
    available_plans: Optional[List[Price]]

class SubscriptionStatusSerializer(serializers.Serializer):
    available_plans = PriceSerializer(many=True, required=False, read_only=True)
