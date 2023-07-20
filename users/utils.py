from typing import Optional
import logging

import boto3
from botocore.exceptions import ClientError
import uuid
import os

from django.template.loader import render_to_string

from grammargrove.utils import get_base_url_for_environment
from .models import User, UserStatus, UserLoginEmail, PracticeReminderEmail
from userpreferences.models import UserPreferences

def _get_sender_email_format(
    sender_email_name: str,
    sender_email_address: Optional[str] = None
) -> str:
    if not sender_email_address:
        sender_email_address = os.environ["SES_DEFAULT_SENDER_ADDRESS"]
    return f"{sender_email_name} <{sender_email_address}>"


def _send_email_to_user(
    to_address: str,
    source_address: str,
    subject: str,
    html_message: str,
) -> bool:
    client = boto3.client(
        'ses',
        region_name=os.environ.get("SES_REGION", "us-east-1"),
        aws_access_key_id=os.environ["SES_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["SES_SECRET_ACCESS_KEY"]
    )
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    to_address,
                ],
            },
            Message={
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': html_message,
                    },
                },
            },
            Source=source_address
        )
    except ClientError as e:
        logging.info(e.response['Error']['Message'])
        return True
    else:
        logging.info("Email sent! Message ID:"),
        logging.info(response['MessageId'])
    return False

def send_verifcation_email_to_user(login_email: UserLoginEmail) -> bool:
    """Takes in a user and returns whether or not this send is retryable"""
    client = boto3.client(
        'ses',
        region_name=os.environ.get("SES_REGION", "us-east-1"),
        aws_access_key_id=os.environ["SES_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["SES_SECRET_ACCESS_KEY"]
    )
    user_id = login_email.user.id
    users = User.objects.filter(pk=user_id)
    if not users:
        logging.warning(f"User {user_id} does not exist")
        return False
    elif len(users) > 1:
        logging.warning(f"User ID {user_id} returned multiple users")
        return False
    user = users[0]
    if user.status != UserStatus.UNVERIFIED:
        logging.info(f"User {user_id} is already verified, skipping")
        return False
    base_url = f"{get_base_url_for_environment()}/api/users/v1"
    unsubscribe_link = f"{base_url}/{user_id}/unsubscribe/"
    verification_link = f"{base_url}/{login_email.id}/verify/"
    html_message = render_to_string('verification-email.html', {
        'unsubscribe_link': unsubscribe_link,
        'verification_link': verification_link,
    })
    source = _get_sender_email_format("GrammarGrove Accounts")
    return _send_email_to_user(
        user.email,
        source,
        'Verify your email address',
        html_message
    )


def send_login_email_to_user(login_email: UserLoginEmail) -> bool:
    """Takes in a user and returns whether or not this send is retryable"""
    user_id = login_email.user.id
    users = User.objects.filter(pk=user_id)
    if not users:
        logging.warning(f"User {user_id} does not exist")
        return False
    elif len(users) > 1:
        logging.warning(f"User ID {user_id} returned multiple users")
        return False
    user = users[0]
    if user.status == UserStatus.UNVERIFIED:
        logging.info(f"User {user_id} is unverified, sending verification email instead")
        return send_verifcation_email_to_user(login_email)
    elif user.has_usable_password():
        logging.info(f"User {user_id} has valid password, skipping")
        return False
    base_url = f"{get_base_url_for_environment()}/api/users/v1"
    unsubscribe_link = f"{base_url}/{user_id}/unsubscribe/"
    login_link = f"{base_url}/{login_email.id}/login/"
    html_message = render_to_string('login-email.html', {
        'unsubscribe_link': unsubscribe_link,
        'login_link': login_link,
    })
    source = _get_sender_email_format("GrammarGrove Accounts")
    return _send_email_to_user(
        user.email,
        source,
        'Login to GrammarGrove',
        html_message
    )


def send_daily_practice_email(practice_reminder_email: PracticeReminderEmail) -> bool:
    user =  practice_reminder_email.user
    preferences = UserPreferences.objects.filter(user=user)
    if user.status != UserStatus.VERIFIED or len(preferences) and not preferences[0].daily_practice_reminders_enabled:
        return False
    base_url = f"{get_base_url_for_environment()}/api/users/v1"
    unsubscribe_link = f"{base_url}/{user.id}/unsubscribe/"
    login_link = f"{base_url}/{practice_reminder_email.id}/gotoquiz/"
    html_message = render_to_string('practice-reminder-email.html', {
        'unsubscribe_link': unsubscribe_link,
        'login_link': login_link,
    })
    source = _get_sender_email_format("GrammarGrove Daily Practice Reminder")
    return _send_email_to_user(
        user.email,
        source,
        'Time to practice Mandarin',
        html_message
    )
