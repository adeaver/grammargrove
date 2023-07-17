from django.contrib import admin

from .models import (
    User,
    UserLoginEmail,
    PracticeReminderEmail,
    PracticeReminderEmailAdmin,
)

admin.site.register(User)
admin.site.register(UserLoginEmail)
admin.site.register(PracticeReminderEmail, PracticeReminderEmailAdmin)
