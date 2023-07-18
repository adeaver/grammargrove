from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from grammargrove.text_utils import has_hanzi
from words.models import Definition


class Command(BaseCommand):
    help = "Marks definitions containing hanzi"

    def handle(self, *args, **options):
        for d in Definition.objects.all():
            contains_hanzi = has_hanzi(d.definition)
            is_valid = len(d.definition.strip()) > 0
            if contains_hanzi or not is_valid:
                d.contains_hanzi = contains_hanzi
                d.is_valid = is_valid
                d.save()

