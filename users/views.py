import json
import uuid
import logging
import datetime
from enum import Enum
from typing import Optional
from django.db import IntegrityError

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import User, UserStatus, UserLoginEmail, UserLoginEmailType
from grammargrove.tasks import send_login_email

class SearchEmailAction(Enum):
    RequireLogin = 'require-login'
    RequireSignup = 'require-signup'
    Redirect = 'redirect'

class UserViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['get'])
    def verify(self, request: HttpRequest, pk: Optional[str] = None) -> HttpResponse:
        user_login_email_id = uuid.UUID(pk)
        emails = User.objects.filter(pk=user_id)
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
        return redirect("/dashboard/")


    @action(detail=True, methods=['get'])
    def login(self, request: HttpRequest, pk: Optional[str] = None) -> HttpResponse:
        user_login_email_id = uuid.UUID(pk)
        emails = User.objects.filter(pk=user_id)
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
        user = authenticate(username=user.email)
        if user:
            email.expires_at = datetime.now()
            return redirect("/dashboard/")
        return redirect("/?error=bad_auth")


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
        user.status = UserStatus.UNSUBSCRIBED
        user.save()
        return redirect("/")


    @action(detail=False, methods=['post'])
    def search_by_email(self, request: HttpRequest) -> JsonResponse:
        email = request.data["email"]
        users = User.objects.filter(email=email)
        user = None if not users else users[0]
        action = SearchEmailAction.RequireLogin
        if not user:
            if request.user:
                logout(request)
            action = SearchEmailAction.RequireSignup
            new_user = User(email=email)
            new_user.save()
            login_email = UserLoginEmail(user=new_user, email_type=UserLoginEmailType.VERIFICATION)
            try:
                login_email.save()
                send_login_email(str(login_email.id))
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
                    send_login_email(str(login_email.id))
                except IntegrityError:
                    logging.info("User already has a login email, skipping")
            elif not user.has_usable_password():
                action = SearchEmailAction.RequireSignup
                login_email = UserLoginEmail(user=user, email_type=UserLoginEmailType.LOGIN)
                try:
                    login_email.save()
                    send_login_email(str(login_email.id))
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
                    send_login_email(str(login_email.id))
                except IntegrityError:
                    logging.info("User already has a login email, skipping")
            elif not user.has_usable_password():
                action = SearchEmailAction.RequireSignup
                login_email = UserLoginEmail(user=user, email_type=UserLoginEmailType.LOGIN)
                try:
                    login_email.save()
                    send_login_email(str(login_email.id))
                except IntegrityError:
                    logging.info("User already has a login email, skipping")
        else:
            raise AssertionError("Unreachable")
        return JsonResponse({"action": action.value})
