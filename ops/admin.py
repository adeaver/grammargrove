from django.contrib import admin
from .featureflags import FeatureFlag, FeatureFlagAdmin

admin.site.register(FeatureFlag, FeatureFlagAdmin)
