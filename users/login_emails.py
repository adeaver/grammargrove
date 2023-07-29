from typing import List, Optional

import logging
from uuid import UUID

from django.utils import timezone
from django.db import transaction

from .utils import send_login_email_to_user, send_verifcation_email_to_user
from .models import UserLoginEmail, UserLoginEmailType

def get_outstanding_login_emails() -> List[UUID]:
    return list(
        UserLoginEmail.objects.filter(
            fulfilled=False, expires_at__gt=timezone.now()
        )
        .values_list("id", flat=True)
    )


def fulfill_login_email_by_id(login_email_id: UUID) -> bool:
    with transaction.atomic():
        retryable = False
        login_email = UserLoginEmail.objects.filter(id=login_email_id, fulfilled=False, expires_at__gt=timezone.now()).first()
        if not login_email:
            logging.warn(f"{login_email_id} is invalid, skipping")
            return False
        if login_email.is_expired():
            logging.warn(f"UserLoginEmail {login_email_id} is expired, skipping")
            return False
        elif login_email.is_fulfilled():
            logging.warn(f"UserLoginEmail {login_email_id} is already fulfilled, skipping")
            return False
        elif login_email.email_type == UserLoginEmailType.LOGIN:
            logging.warn(f"Attempting to send login type UserLoginEmail {login_email_id}")
            retryable = send_login_email_to_user(login_email)
        elif login_email.email_type == UserLoginEmailType.VERIFICATION:
            logging.warn(f"Attempting to send verification type UserLoginEmail {login_email_id}")
            retryable = send_verifcation_email_to_user(login_email)
        if retryable:
            return True
        login_email.fulfilled = True
        login_email.save()
        return False
