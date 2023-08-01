import json
import uuid
import logging
import requests
import datetime
from enum import Enum
from typing import Optional
from django.db import IntegrityError

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import User, UserStatus, UserLoginEmail, UserLoginEmailType, PracticeReminderEmail
from userpreferences.models import UserPreferences

from grammargrove.tasks import fulfill_login_email

from ops.models import FeatureFlagName
from ops.featureflags import get_boolean_feature_flag

class SearchEmailAction(Enum):
    RequireLogin = 'require-login'
    RequireSignup = 'require-signup'
    Redirect = 'redirect'

class UserViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['get'])
    def verify(self, request: HttpRequest, pk: Optional[str] = None) -> HttpResponse:
        user_login_email_id = uuid.UUID(pk)
        emails = UserLoginEmail.objects.filter(pk=user_login_email_id)
        if not emails:
            return HttpResponseBadRequest()
        elif len(emails) > 1:
            logging.warning(f"User Login Email ID {user_login_email_id} returned {len(emails)} results, but expected at most 1")
            return HttpResponseServerError()
        email = emails[0]
        if email.is_expired():
            logging.warning(f"User Login Email ID {user_login_email_id} is expired")
            return redirect("/?error=expired_auth")
        user = User.objects.get(pk=email.user.id)
        user.status = UserStatus.VERIFIED
        user.save()
        login(request, user)
        return redirect("/onboarding/")


    @action(detail=True, methods=['get'])
    def gotoquiz(self, request: HttpRequest, pk: Optional[str] = None) -> HttpResponse:
        user_practice_reminder_email_id = uuid.UUID(pk)
        emails = PracticeReminderEmail.objects.filter(pk=user_practice_reminder_email_id)
        if not emails:
            return HttpResponseBadRequest()
        elif len(emails) > 1:
            logging.warning(f"User Login Email ID {user_practice_reminder_email_id} returned {len(emails)} results, but expected at most 1")
            return HttpResponseServerError()
        email = emails[0]
        if email.is_expired():
            logging.warning(f"User Login Email ID {user_practice_reminder_email_id} is expired")
            return redirect("/?error=expired_auth")

        user = User.objects.get(pk=email.user.id)
        def handle_redirect():
            if user.has_usable_password():
                return redirect("/")
            login(request, user)
            return redirect("/quiz/")

        if request.user is not None:
            if user.id == request.user.id:
                # user is currently logged in
                return redirect("/quiz/")
            # wrong user is currently logged in
            logout(request)
        return handle_redirect()


    @action(detail=True, methods=['get'])
    def login(self, request: HttpRequest, pk: Optional[str] = None) -> HttpResponse:
        user_login_email_id = uuid.UUID(pk)
        emails = UserLoginEmail.objects.filter(pk=user_login_email_id)
        if not emails:
            return HttpResponseBadRequest()
        elif len(emails) > 1:
            logging.warning(f"User Login Email ID {user_login_email_id} returned {len(emails)} results, but expected at most 1")
            return HttpResponseServerError()
        email = emails[0]
        if email.is_expired():
            logging.warning(f"User Login Email ID {user_login_email_id} is expired")
            return redirect("/?error=expired_auth")
        user = User.objects.get(pk=email.user.id)
        if user.has_usable_password():
            return redirect("/")
        login(request, user)
        email.expires_at = datetime.datetime.now()
        email.save()
        return redirect("/dashboard/")


    @action(detail=True, methods=['get'])
    def unsubscribe(self, request: HttpRequest, pk: Optional[str] = None) -> HttpResponse:
        user_id = uuid.UUID(pk)
        users = User.objects.filter(pk=user_id)
        if not users:
            return HttpResponseBadRequest()
        elif len(users) > 1:
            logging.warning(f"User ID {user_id} returned {len(users)} results, but expected at most 1")
            return HttpResponseServerError()
        user = users[0]
        preferences = UserPreferences.objects.filter(user=user)
        prefs = preferences[0] if preferences else UserPreferences(user=user)
        prefs.set_unsubscribed_from_emails()
        prefs.save()
        return redirect("/")


    @action(detail=False, methods=['post'])
    def search_by_email(self, request: HttpRequest) -> JsonResponse:
        token = request.data["token"]
        if get_boolean_feature_flag(FeatureFlagName.RecaptchaEnabled):
            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                "response": token,
                "secret": settings.GRECAPTCHA_SECRET_KEY,
            })
            result_json = resp.json()
            if not result_json.get('success'):
                return HttpResponseBadRequest()
        email = request.data["email"]
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponseBadRequest()
        users = User.objects.filter(email=email)
        user = None if not users else users[0]
        action = SearchEmailAction.RequireLogin
        if not user:
            if request.user:
                logout(request)
            action = SearchEmailAction.RequireSignup
            new_user = User.objects.create_user(email=email)
            login_email = UserLoginEmail(user=new_user, email_type=UserLoginEmailType.VERIFICATION)
            try:
                login_email.save()
                fulfill_login_email.spool(
                    { "login_email_id".encode("utf-8"): str(login_email.id).encode("utf-8") }
                )
            except IntegrityError:
                logging.info("User already has a login email, skipping")
        elif request.user and request.user.id != user.id:
            # The logged in user has entered another email
            logout(request)
            action = SearchEmailAction.RequireLogin
            if user.status == UserStatus.UNVERIFIED:
                action = SearchEmailAction.RequireSignup
                login_email = UserLoginEmail(user=user, email_type=UserLoginEmailType.VERIFICATION)
                try:
                    login_email.save()
                    fulfill_login_email.spool(
                        { "login_email_id".encode("utf-8"): str(login_email.id).encode("utf-8") }
                    )
                except IntegrityError:
                    logging.info("User already has a login email, skipping")
            elif not user.has_usable_password():
                action = SearchEmailAction.RequireSignup
                login_email = UserLoginEmail(user=user, email_type=UserLoginEmailType.LOGIN)
                try:
                    login_email.save()
                    fulfill_login_email.spool(
                        { "login_email_id".encode("utf-8"): str(login_email.id).encode("utf-8") }
                    )
                except IntegrityError:
                    logging.info("User already has a login email, skipping")
        elif request.user and request.user.id == user.id:
            action = SearchEmailAction.Redirect
        elif not request.user:
            action = SearchEmailAction.RequireLogin
            if user.status == UserStatus.UNVERIFIED:
                action = SearchEmailAction.RequireSignup
                login_email = UserLoginEmail(user=user, email_type=UserLoginEmailType.VERIFICATION)
                try:
                    login_email.save()
                    fulfill_login_email.spool(
                        { "login_email_id".encode("utf-8"): str(login_email.id).encode("utf-8") }
                    )
                except IntegrityError:
                    logging.info("User already has a login email, skipping")
            elif not user.has_usable_password():
                action = SearchEmailAction.RequireSignup
                login_email = UserLoginEmail(user=user, email_type=UserLoginEmailType.LOGIN)
                try:
                    login_email.save()
                    fulfill_login_email.spool(
                        { "login_email_id".encode("utf-8"): str(login_email.id).encode("utf-8") }
                    )
                except IntegrityError:
                    logging.info("User already has a login email, skipping")
        else:
            raise AssertionError("Unreachable")
        return JsonResponse({"action": action.value})
