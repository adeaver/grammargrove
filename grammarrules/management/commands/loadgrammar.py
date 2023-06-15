import logging
import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = "Loads the grammar rules"

    def handle(self, *args, **options):
        with open(f"{settings.BASE_DIR}/grammarrules/data/grammarrules.csv", "r") as f:
            grammar_rule_reader = csv.reader(f)
            for row in grammar_rule_reader:
                print(row)


