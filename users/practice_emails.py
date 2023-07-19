from typing import Optional
import logging

from datetime import timedelta
from django.utils import timezone
from django.db import transaction, IntegrityError

from .models import User, UserStatus, PracticeReminderEmail
from .utils import send_daily_practice_email

def create_all_practice_emails():
    users = User.objects.filter(status=UserStatus.VERIFIED)
    send_at = timezone.now()
    send_at = send_at.replace(hour=13, minute=0, second=0, microsecond=0)
    unique_key = f"{send_at.year}:{send_at.month}:{send_at.day}"
    for user in users:
        with transaction.atomic():
            existing_emails = PracticeReminderEmail.objects.filter(user=user, unique_key=unique_key)
            if not existing_emails:
                PracticeReminderEmail(
                    user=user,
                    unique_key=unique_key,
                    send_at=send_at
                ).save()


def send_outstanding_practice_reminders():
    should_exit = False
    while not should_exit:
        with transaction.atomic():
            r = _lookup_outstanding_practice_reminder()
            if not r:
                should_exit = True
                break
            r.fulfilled = True
            r.expires_at = timezone.now() + timedelta(hours=25)
            r.save()
            send_daily_practice_email(r)


def _lookup_outstanding_practice_reminder() -> Optional[PracticeReminderEmail]:
    outstanding_practice_reminders = PracticeReminderEmail.objects.filter(
        fulfilled=False, send_at__lt=timezone.now()
    )
    if not outstanding_practice_reminders:
        return None
    return outstanding_practice_reminders[0]
