from django.contrib import admin

from .models import UserPreferences, UserPreferencesAdmin

admin.site.register(UserPreferences, UserPreferencesAdmin)
