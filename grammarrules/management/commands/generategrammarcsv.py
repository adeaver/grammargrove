from typing import List, Union, NamedTuple

import logging

import requests
import codecs
import string

from bs4 import BeautifulSoup, Tag

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

BASE_URL = "https://resources.allsetlearning.com"

class Command(BaseCommand):
    help = "Loads the grammar rules"

    def handle(self, *args, **options):
        #  hsk_levels = [1, 2, 3, 4, 5, 6]
        grammar_rules_csv_lines = []
        example_csv_lines = []
        hsk_levels = [1]
        for level in hsk_levels:
            html = _get_html_for_hsk_level(level)
            rules = _get_rules_from_html(html)
            for r in rules:
                csv_lines = r.get_csv_lines()
                grammar_rules_csv_lines.append(
                    csv_lines.to_text(level)
                )
                for e in csv_lines.examples:
                    example_csv_lines.append(
                        e.to_text(len(grammar_rules_csv_lines))
                    )



def _make_text(encoded_text: str) -> str:
    hex_str, _ = codecs.escape_decode(encoded_text, 'hex')
    return hex_str.decode("utf-8")


def _get_text_from_element_list(contents: List[Union[str, Tag]]) -> str:
    elements = ' '.join([ _get_text_from_element_list(c.contents) if isinstance(c, Tag) else c for c in contents ])
    return _make_text(elements).replace("\n", "").strip()


def _get_html_for_hsk_level(level: int) -> str:
    if level == 1:
        with open(f"{settings.BASE_DIR}/resp.txt") as f:
            return f.read()
    request_url = f"{BASE_URL}/chinese/grammar/HSK_{level}_grammar_points"
    resp = requests.get(request_url)
    return resp.content


class ProcessedExample(NamedTuple):
    example_structure: str
    use: str
    hanzi: str
    pinyin: str
    explanation: str

    def to_text(self, line_number: int) -> str:
        return f'{line_number},"{self.example_structure}","{self.use}","{self.hanzi}","{self.pinyin}","{self.explanation}"'

class CSVLine(NamedTuple):
    title: str
    definition: str
    structure: str
    structure_pinyin: str

    examples: List[ProcessedExample]

    def to_text(self, level: int) -> str:
        return f'"{self.title}","{self.definition}","{self.structure}","{self.structure_pinyin}",{level}'

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
        primary_structure = processed_structures[primary_idx]

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
            use = input(
                "What is the use for this example?\n\n" +
                ">>> "
            )
            if not use.strip():
                use = definition
            examples.append(ProcessedExample(
                example_structure=processed_structures[struct_idx],
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
