from typing import Dict

from django.db import transaction
from .models import FeatureFlag, FeatureFlagName, FeatureFlagType

_DEFAULT_BOOLEAN_VALUES: Dict[FeatureFlagName, bool]  = {
    FeatureFlagName.GrammarRuleFetchesEnabled: False,
    FeatureFlagName.PracticeReminderEmailsEnabled: True,
    FeatureFlagName.RecaptchaEnabled: False,
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


def initialize_feature_flags():
    for feature_flag in FeatureFlagName:
        if _is_set(feature_flag):
            continue
        flag_type = feature_flag.get_type()
        if flag_type == FeatureFlagType.Boolean:
            set_boolean_feature_flag(feature_flag, _DEFAULT_BOOLEAN_VALUES[feature_flag])
        else:
            raise ValueError(f"Unrecognized flag type {flag_type}")

def _is_set(name: FeatureFlagName) -> bool:
    return FeatureFlag.objects.filter(id=name).first() is not None
