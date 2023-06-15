from typing import Dict, Optional, Tuple

neutral_tone_characters = { 'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u', 'ü': 'u:' }
first_tone_characters = { 'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u', 'ǖ': 'u:' }
second_tone_characters = { 'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ǘ': 'u:' }
third_tone_characters = { 'ǎ': 'a', 'ě': 'e', 'ǐ': 'i', 'ǒ': 'o', 'ǔ': 'u', 'ǚ': 'u:' }
fourth_tone_characters = { 'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u', 'ǜ': 'u:' }

def _get_first_vowel_with_index(pinyin: str) -> Tuple[str, int]:
    for idx, c in enumerate(pinyin):
        if c in first_tone_characters:
            return first_tone_characters[c], idx
        elif c in second_tone_characters:
            return second_tone_characters[c], idx
        elif c in third_tone_characters:
            return third_tone_characters[c], idx
        elif c in fourth_tone_characters:
            return fourth_tone_characters[c], idx
        elif c in neutral_tone_characters:
            character = neutral_tone_characters[c]
            if (
                character == 'u' and
                (idx+1) < len(pinyin) and
                pinyin[idx+1] == ":"
            ):
                return 'u:', idx
            return character, idx
    raise ValueError(f"Invalid pinyin {pinyin}")

def _get_replacement_vowel_in_display_form(vowel: str, tone_number: int) -> str:
    tone_dict: Dict[str, str] = neutral_tone_characters
    if tone_number == 1:
        tone_dict = first_tone_characters
    elif tone_number == 2:
        tone_dict = second_tone_characters
    elif tone_number == 3:
        tone_dict = third_tone_characters
    elif tone_number == 4:
        tone_dict = fourth_tone_characters
    elif tone_number == 5:
        pass
    else:
        raise AssertionError(f"Tone Number {tone_number} is not valid")
    for display, base in tone_dict.items():
        if base == vowel:
            return display
    raise ValueError(f"Vowel {vowel} and tone {tone_number} not found")

def get_tone_number_from_display_form(pinyin: str) -> Optional[int]:
    for c in pinyin:
        if c in first_tone_characters:
            return 1
        elif c in second_tone_characters:
            return 2
        elif c in third_tone_characters:
            return 3
        elif c in fourth_tone_characters:
            return 4
        elif c.isnumeric():
            return None
    return 5 if pinyin[-1].isalpha() else None

def is_display_form(pinyin: str) -> bool:
    return get_tone_number_from_display_form(pinyin) is not None

def convert_to_display_form(pinyin: str) -> str:
    if is_display_form(pinyin):
        return pinyin
    tone_number = get_tone_number_from_numeric_form(pinyin)
    if tone_number is None:
        raise ValueError(f"Pinyin {pinyin} is neither numeric nor display form")
    vowel, idx = _get_first_vowel_with_index(pinyin)
    replacement_vowel = _get_replacement_vowel_in_display_form(vowel, tone_number)
    return f"{pinyin[:idx]}{replacement_vowel}{pinyin[idx+1+len(vowel):]}"

def get_tone_number_from_numeric_form(pinyin: str) -> Optional[int]:
    if pinyin[-1].isnumeric():
        return int(pinyin[-1])
    return None

def is_numeric_form(pinyin: str) -> bool:
    return get_tone_number_from_numeric_form(pinyin) is not None

def convert_to_numeric_form(pinyin: str) -> bool:
    if is_numeric_form(pinyin):
        return pinyin
    tone_number = get_tone_number_from_display_form(pinyin)
    if tone_number is None:
        raise ValueError(f"Pinyin {pinyin} is neither numeric nor display form")
    vowel, idx = _get_first_vowel_with_index(pinyin)
    return f"{pinyin[:idx]}{vowel}{pinyin[idx+1:]}{tone_number}"

