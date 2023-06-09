from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import User

class UserViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['post'])
    def search_by_email(self, request: HttpRequest) -> JsonResponse:
        email = request.POST["email"]
        user = User.objects.filter(email=email)[0]
        # TODO: if user doesn't exist, log out current user
        # create new user, enqueue email task, and redirect to dashboard
        #
        # if user does exist, if it's the logged in user, redirect to dashboard
        # if not, log that user out and show password field
        user_does_not_exist = not user
        return JsonResponse({"found": not user_does_not_exist})
