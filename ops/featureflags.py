from typing import Dict

from django.db import transaction
from .models import FeatureFlag, FeatureFlagName, FeatureFlagType

_DEFAULT_BOOLEAN_VALUES: Dict[FeatureFlagName, bool]  = {
    FeatureFlagName.GrammarRuleFetchesEnabled: False
}

def get_boolean_feature_flag(name: FeatureFlagName) -> bool:
    assert name.get_type() == FeatureFlagType.Boolean
    assert name in _DEFAULT_BOOLEAN_VALUES
    flags = FeatureFlag.objects.filter(id=name)
    if not flags:
        return _DEFAULT_BOOLEAN_VALUES[name]
    value = flags.first().enabled
    assert value is not None
    return value


def set_boolean_feature_flag(name: FeatureFlagName, value: bool) -> None:
    assert name.get_type() == FeatureFlagType.Boolean
    with transaction.atomic():
        FeatureFlag.objects.filter(id=name).delete()
        FeatureFlag(id=name, enabled=value).save()
