import logging

from datetime import timedelta
from django.utils import timezone
from django.db import transaction, IntegrityError

from .models import User, UserStatus, PracticeReminderEmail
from .utils import send_daily_practice_email

def create_all_practice_emails():
    users = User.objects.filter(status=UserStatus.VERIFIED)
    for user in users:
        send_at = timezone.now()
        send_at = send_at.replace(hour=13, minute=0, second=0, microsecond=0)
        unique_key = f"{send_at.year}:{send_at.month}:{send_at.day}"
        try:
            PracticeReminderEmail(
                user=user,
                unique_key=unique_key,
                send_at=send_at
            ).save()
        except IntegrityError:
            continue


def send_outstanding_practice_reminders():
    outstanding_practice_reminders = PracticeReminderEmail.objects.filter(
        fulfilled=False, send_at__lt=timezone.now()
    )
    for r in outstanding_practice_reminders:
        with transaction.atomic():
            r.fulfilled = True
            r.expires_at = timezone.now() + timedelta(hours=25)
            r.save()
            send_daily_practice_email(r)
