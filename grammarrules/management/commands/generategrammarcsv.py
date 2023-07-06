from typing import List, Union, NamedTuple, Dict

import logging

import requests
import codecs
import string
import csv

from bs4 import BeautifulSoup, Tag

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

BASE_URL = "https://resources.allsetlearning.com"

REPLACEMENTS = {
    "subj.": "subject",
    "verb": "verb",
    "adj.": "adjective",
    "obj.": "object",
    "adv.": "adverb",
    "noun": "noun",
}

class Command(BaseCommand):
    help = "Loads the grammar rules"

    def add_arguments(self, parser):
        parser.add_argument(
            "--level",
            help="Which level to update",
        )
        parser.add_argument(
            "--start_at_rule",
            help="Which rule to start at",
        )

    def handle(self, *args, **options):
        level = 1 if not options["level"] else int(options.get("level"))
        start_at_rule = -1 if not options["start_at_rule"] else int(options.get("start_at_rule"))
        mode = "w" if start_at_rule == -1 else "a"
        number_of_rules = 0
        html = _get_html_for_hsk_level(level)
        rules = _get_rules_from_html(html)
        with open(f"{settings.BASE_DIR}/grammarrules/data/grammarrules_{level}.csv", mode) as rules_file:
            with open(f"{settings.BASE_DIR}/grammarrules/data/grammarruleexamples_{level}.csv", mode) as examples_file:
                rules_writer = csv.DictWriter(rules_file, fieldnames=["title", "definition", "hanzi", "pinyin", "level"])
                if mode == "w":
                    rules_writer.writeheader()

                examples_writer = csv.DictWriter(examples_file, fieldnames=["grammar_rule_line_number", "structure", "use", "hanzi", "pinyin", "explanation"])

                if mode == "w":
                    examples_writer.writeheader()

                for r in rules:
                    if number_of_rules <= start_at_rule:
                        number_of_rules += 1
                        continue
                    try:
                        csv_lines = r.get_csv_lines()
                    except KeyboardInterrupt:
                        return
                    except Exception as e:
                        logging.warn(f"Error: {e}")
                        continue
                    rules_writer.writerow(
                        csv_lines.as_row(level)
                    )
                    number_of_rules += 1
                    for e in csv_lines.examples:
                        examples_writer.writerow(
                            e.as_row(number_of_rules)
                        )



def _make_text(encoded_text: str) -> str:
    hex_str, _ = codecs.escape_decode(encoded_text, 'hex')
    return hex_str.decode("utf-8")


def _get_text_from_element_list(contents: List[Union[str, Tag]]) -> str:
    elements = ' '.join([ _get_text_from_element_list(c.contents) if isinstance(c, Tag) else c for c in contents ])
    return _make_text(elements).replace("\n", "").strip()


def _get_html_for_hsk_level(level: int) -> str:
    request_url = f"{BASE_URL}/chinese/grammar/HSK_{level}_grammar_points"
    resp = requests.get(request_url)
    return resp.content


class ProcessedExample(NamedTuple):
    example_structure: str
    use: str
    hanzi: str
    pinyin: str
    explanation: str

    def as_row(self, rule_line_number: int) -> Dict[str, str]:
        return {
            "grammar_rule_line_number": rule_line_number,
            "structure": self.example_structure,
            "use": self.use,
            "hanzi": self.hanzi,
            "pinyin": self.pinyin,
            "explanation": self.explanation
        }

class CSVLine(NamedTuple):
    title: str
    definition: str
    structure: str
    structure_pinyin: str

    examples: List[ProcessedExample]

    def as_row(self, level: int) -> Dict[str, str]:
        return {
            "title": self.title,
            "definition": self.definition,
            "hanzi": self.structure,
            "pinyin": self.structure_pinyin,
            "level": str(level),
        }

class Example(NamedTuple):
    hanzi: str
    translation: str
    pinyin: str

class Rule(NamedTuple):
    title: str
    next_url: str
    structure: str
    example: str

    def get_html(self) -> str:
        resp = requests.get(self.next_url)
        return resp.content

    def get_csv_lines(self) -> CSVLine:
        logging.warn(f"**** PROCESSING {self.next_url} ****")
        html = self.get_html()
        soup = BeautifulSoup(html)
        structures = soup.find_all("div", attrs = { 'class': 'jiegou' })
        example_containers = soup.find_all("div", attrs = { 'class': 'liju' })
        examples = []
        for ec in example_containers:
            examples += ec.find_all("li")

        processed_structures = [
            _get_text_from_element_list(s)
            for s in structures
        ]

        processed_examples: List[Example] = []
        for e in examples:
            text = _get_text_from_element_list(e)
            pinyin_element = e.find("span", attrs = { 'class': 'pinyin' })
            if not pinyin_element:
                continue
            pinyin = _get_text_from_element_list(pinyin_element)
            translation_element = e.find("span", attrs = { 'class': 'trans' })
            if not translation_element:
                continue
            translation = _get_text_from_element_list(translation_element)
            text = text.replace(pinyin, "")
            text = text.replace(translation, "")
            processed_examples.append(
                Example(
                    hanzi=text,
                    pinyin=pinyin,
                    translation=translation
                )
            )

        change_to_title = input(
            "\nWould you like to edit the title of:\n" +
            self.title + "\n\n" +
            ">>> "
        )
        title = self.title
        if change_to_title.strip():
            title = change_to_title

        definition = self.title
        change_to_definition = input(
            "\nWould you like to edit the definition of:\n" +
            self.title + "\n\n" +
            ">>> "
        )
        if change_to_definition.strip():
            definition = change_to_definition


        primary_idx = 0
        if len(processed_structures) > 1:
            primary_idx = int(
                input(
                    "\nWhich is the primary structure?\n" +
                    "\n".join([ f"{idx}. {p}" for idx, p in enumerate(processed_structures)]) + "\n" +
                    ">>> "
                )
            )
        primary_structure = " + ".join([ REPLACEMENTS[p.lower().strip()] if p.lower().strip() in REPLACEMENTS else p.strip() for p in processed_structures[primary_idx].split("+") ])


        structure_pinyin = input(
            "\nWhat's the pinyin for:\n" +
            primary_structure + "\n\n" +
            ">>> "
        )

        examples: List[ProcessedExample] = []
        for p in processed_examples:
            answer = input(
                "\nWould you like to use the following example?\n\n" +
                p.hanzi + "\n" +
                f"({p.pinyin})\n" +
                p.translation + "\n\n" +
                "(y/n) >>> "
            )
            if answer.lower().strip() == "break":
                break
            elif answer.lower().strip() != "y":
                continue
            struct_idx = 0
            if len(processed_structures) > 1:
                struct_idx = int(
                    input(
                        "\nWhich is the primary structure for this example?\n" +
                        "\n".join([ f"{idx}. {p}" for idx, p in enumerate(processed_structures)]) + "\n" +
                        ">>> "
                    )
                )
            structure = " + ".join([ REPLACEMENTS[p.lower().strip()] if p.lower().strip() in REPLACEMENTS else p.strip() for p in processed_structures[struct_idx].split("+") ])
            structure_change = input(
                "\nWould you like to update the structure for this example?\n" +
                f"It’s currently {structure}\n\n" +
                ">>> "
            )
            if structure_change.strip():
                structure = structure_change.strip()
            use = input(
                "What is the use for this example?\n" +
                f"Default: {definition}\n\n" +
                ">>> "
            )
            if not use.strip():
                use = definition
            examples.append(ProcessedExample(
                example_structure=structure,
                use=use,
                hanzi=p.hanzi.translate
                    (str.maketrans('', '', string.punctuation)),
                pinyin=p.pinyin.translate
                    (str.maketrans('', '', string.punctuation)),
                explanation=f"explains that {p.translation.lower()}",
            ))
        return CSVLine(
            title=title,
            definition=definition,
            structure=primary_structure,
            structure_pinyin=structure_pinyin,
            examples=examples,
        )

def _get_rules_from_html(html: str) -> List[Rule]:
    out: List[Rule] = []
    soup = BeautifulSoup(html)
    tables = soup.find_all('table', attrs = { 'class': 'wikitable' })
    for t in tables:
        rows = t.find_all('tr')
        for idx, row in enumerate(rows):
            if idx == 0:
                continue
            cells = row.find_all('td')
            title, structure, example = cells
            title_anchor = title.find('a')
            next_url = title_anchor["href"]
            out.append(
                Rule(
                    title=_get_text_from_element_list(title_anchor),
                    next_url=f"{BASE_URL}{next_url}",
                    structure=_get_text_from_element_list(structure),
                    example=_get_text_from_element_list(example.contents),
                )
            )
    return out
