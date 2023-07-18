from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from grammargrove.text_utils import has_hanzi
from words.models import Definition


class Command(BaseCommand):
    help = "Marks definitions containing hanzi"

    def handle(self, *args, **options):
        for d in Definition.objects.all():
            if has_hanzi(d.definition):
                d.contains_hanzi = True
                d.save()

