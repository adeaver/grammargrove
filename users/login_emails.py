from typing import Optional

import logging
from uuid import UUID

from django.utils import timezone
from django.db import transaction

from .utils import send_login_email_to_user, send_verifcation_email_to_user
from .models import UserLoginEmail, UserLoginEmailType

def fulfill_all_login_emails():
    while True:
        with transaction.atomic():
            outstanding_login_email = _get_outstanding_login_emails()
            if not outstanding_login_email:
                return
            _fulfill_login_email_by_id(outstanding_login_email.id)



def _fulfill_login_email_by_id(login_email_id: UUID) -> bool:
    retryable = False
    login_email = UserLoginEmail.objects.filter(id=login_email_id).first()
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

def _get_outstanding_login_emails() -> Optional[UserLoginEmail]:
    login_emails = UserLoginEmail.objects.filter(
        fulfilled=False, expires_at__gt=timezone.now()
    )
    return login_emails.first()

