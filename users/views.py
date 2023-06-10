import json
from enum import Enum

from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import User

class SearchEmailAction(Enum):
    RequireLogin = 'require-login'
    RequireSignup = 'require-signup'
    Redirect = 'redirect'

class UserViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def search_by_email(self, request: HttpRequest) -> JsonResponse:
        email = request.data["email"]
        user = User.objects.filter(email=email)[0]
        action = SearchEmailAction.RequireLogin
        if not user:
            if request.user:
                logout(request)
            action = SearchEmailAction.RequireSignup
        elif request.user and request.user.id != user.id:
            # The logged in user has entered another email
            logout(request)
            action = SearchEmailAction.RequireLogin
        elif request.user and request.user.id == user.id:
            action = SearchEmailAction.Redirect
        elif not request.user:
            action = SearchEmailAction.RequireLogin
        else:
            raise AssertionError("Unreachable")
        return JsonResponse({"action": action.value})
