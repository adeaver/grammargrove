from django.contrib import admin
from .models import FeatureFlag, FeatureFlagAdmin

admin.site.register(FeatureFlag, FeatureFlagAdmin)
