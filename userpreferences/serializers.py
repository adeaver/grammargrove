from rest_framework import serializers

from .models import UserPreferences

from billing.permissions import is_user_on_free_trial
from billing.stripe_utils import get_subscription_management_url

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = '__all__'
        read_only_fields = ["user"]

    def to_representation(self, instance: UserPreferences):
        response = super().to_representation(instance)
        if not is_user_on_free_trial(instance.user):
            response["subscription_management_link"] = get_subscription_management_url(
                instance.user
            )
        return response
