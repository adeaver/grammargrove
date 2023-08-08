from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from words.models import LanguageCode, Word, Definition

class Command(BaseCommand):
    help = "Loads the dictionary from CEDICT into a jieba compatible one"

    def handle(self, *args, **options):
        with open(f"{settings.BASE_DIR}/words/data/jieba_simplified.txt", "w") as f:
            f.writelines([
                f"{w.display} 1\n"
                for w in Word.objects.filter(language_code=LanguageCode.SIMPLIFIED_MANDARIN)
            ])
