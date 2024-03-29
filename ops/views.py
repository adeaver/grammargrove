import os

from datetime import datetime

from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from django.http import HttpRequest
from rest_framework.response import Response

from .models import Ping

class OpsViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def version(self, request: HttpRequest) -> Response:
        # Note: this is not entirely accurate locally
        return Response({"version": os.environ.get("GIT_SHA", "unknown")})

    @action(detail=False, methods=["get"])
    def healthcheck(self, request: HttpRequest) -> Response:
        now = datetime.now()
        pings = Ping.objects.order_by("-created_at")
        query_time = datetime.now() - now
        if not pings:
            return Response({}, status.HTTP_503_SERVICE_UNAVAILABLE)
        elif not pings.first().is_ok():
            return Response({}, status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"ok": True, "query_time_usec": query_time.microseconds}, status.HTTP_200_OK)
