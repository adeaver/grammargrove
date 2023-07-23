from django.db import transaction

from .models import Ping

def register_ping():
    with transaction.atomic():
        Ping.objects.all().delete()
        Ping().save()
