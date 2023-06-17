from typing import List, Dict, Optional, Tuple, NamedTuple

import copy
from pygtrie import CharTrie

vowels_by_tone = {
    1: { 'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u', 'ǖ': 'u:' },
    2: { 'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ǘ': 'u:' },
    3: { 'ǎ': 'a', 'ě': 'e', 'ǐ': 'i', 'ǒ': 'o', 'ǔ': 'u', 'ǚ': 'u:' },
    4: { 'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u', 'ǜ': 'u:' },
    5: { 'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u', 'ü': 'u:' },
}

vowels_by_tone_position = {
    "a": 0, "ao": 0, "ai": 0, "an": 0, "ang": 0,
    "o": 0, "ou": 0, "ong": 0,
    "e": 0, "ei": 0, "en": 0, "eng": 0, "er": 0,
    "i": 0, "ia": 1, "iu": 1, "iao": 1, "in": 0, "ing": 0,
    "ian": 1, "iang": 1, "iong": 1,
    "u": 0, "ua": 1, "uo": 1, "ue": 1, "ui": 1, "uai": 1,
    "un": 0, "uan": 1, "uang": 1,
    "u:": 0, "u:e": 2, "u:n": 0, "u:an": 1
}

class _Vowel(NamedTuple):
    vowel: str
    tone_number: int

    def to_display_form(self) -> str:
        skip_next = False
        out = []
        for idx, c in enumerate(self.vowel):
            if skip_next:
                skip_next = False
                continue
            elif (
                c == "u" and
                idx < len(self.vowel)-1
                and self.vowel[idx+1] == ":"
            ):
                c == "u:"
                skip_next=True

            if idx == vowels_by_tone_position[self.vowel]:
                for display, base_form in vowels_by_tone[self.tone_number].items():
                    if base_form == c:
                        out.append(display)
            else:
                out.append(c)
        return "".join(out)


def _is_vowel_and_maybe_tone_number(char: str) -> Tuple[bool, Optional[int]]:
    for tone_number, vowel_dict in vowels_by_tone.items():
        if char in vowel_dict:
            return True, tone_number
    return False, None


def _get_vowel_with_index(pinyin: str) -> Tuple[_Vowel, int]:
    tone_number: int = 5
    all_in_numeric = []
    for c in pinyin:
        is_vowel, char_tone_number = _is_vowel_and_maybe_tone_number(c)
        if is_vowel:
            if char_tone_number != 5:
                tone_number = char_tone_number
            all_in_numeric.append(vowels_by_tone[char_tone_number][c])
        else:
            all_in_numeric.append(c)
    base_version = "".join(all_in_numeric)
    curr_vowel = ""
    curr_vowel_idx = -1
    for vowel in vowels_by_tone_position.keys():
        vowel_idx = base_version.find(vowel)
        if vowel_idx != -1 and len(vowel) > len(curr_vowel):
            curr_vowel = vowel
            curr_vowel_idx = vowel_idx
    assert curr_vowel_idx != -1, (
        f"Could not find any vowels in {pinyin} (base version {base_version})"
    )
    assert curr_vowel != "", (
        f"{pinyin} (base version {base_version}) has no vowels"
    )
    return _Vowel(
        vowel=curr_vowel,
        tone_number=tone_number,
    ), curr_vowel_idx


def _get_replacement_vowel_in_display_form(vowel: str, tone_number: int) -> str:
    for display, base in vowels_by_tone[tone_number].items():
        if base == vowel:
            return display
    raise ValueError(f"Vowel {vowel} and tone {tone_number} not found")

def get_tone_number_from_display_form(pinyin: str) -> Optional[int]:
    for c in pinyin:
        if c.isnumeric():
            return None
        for tone_number in range(4):
            if c in vowels_by_tone[tone_number+1]:
                return tone_number+1
    return 5 if pinyin[-1].isalpha() else None

def is_display_form(pinyin: str) -> bool:
    return get_tone_number_from_display_form(pinyin) is not None

def convert_to_display_form(pinyin: str) -> str:
    if is_display_form(pinyin):
        return pinyin
    tone_number = get_tone_number_from_numeric_form(pinyin)
    if tone_number is None:
        raise ValueError(f"Pinyin {pinyin} is neither numeric nor display form")
    vowel, idx = _get_vowel_with_index(pinyin)
    replacement_vowel = vowel.to_display_form()
    tail_start_pos = idx+1+len(vowel.vowel)
    return f"{pinyin[:idx]}{replacement_vowel}{pinyin[tail_start_pos:]}"

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
    vowel, idx = _get_vowel_with_index(pinyin)
    tail_start_pos = idx+1+len(vowel.to_display_form())
    numeric_form = vowel.vowel
    return f"{pinyin[:idx]}{numeric_form}{pinyin[tail_start_pos:]}{tone_number}"

finals_list = [
    'a', 'ai', 'an', 'ang', 'ao',
    'ba', 'bai', 'ban', 'bang', 'bao', 'bei', 'ben', 'beng',
    'bi', 'bian', 'biang', 'biao', 'bie', 'bin', 'bing', 'bo', 'bu',
    'ca', 'cai', 'can', 'cang', 'cao', 'ce', 'cen', 'ceng',
    'cha', 'chai', 'chan', 'chang', 'chao', 'che', 'chen', 'cheng',
    'chi', 'chong', 'chou', 'chu', 'chua', 'chuai', 'chuan', 'chuang', 'chui', 'chun', 'chuo',
    'ci', 'cong', 'cou', 'cu', 'cuan', 'cui', 'cun', 'cuo',
    'da', 'dai', 'dan', 'dang', 'dao', 'de', 'dei', 'den', 'deng',
    'di', 'dia', 'dian', 'diang', 'diao', 'die', 'ding', 'diu',
    'dong', 'dou', 'du', 'duan', 'dui', 'dun', 'duo',
    'e', 'ei', 'en', 'eng', 'er',
    'fa', 'fan', 'fang', 'fei', 'fen', 'feng', 'fiao',
    'fo', 'fou', 'fu', 'ga', 'gai', 'gan', 'gang', 'gao',
    'ge', 'gei', 'gen', 'geng', 'gong', 'gou',
    'gu', 'gua', 'guai', 'guan', 'guang', 'gui', 'gun', 'guo',
    'ha', 'hai', 'han', 'hang', 'hao', 'he', 'hei', 'hen', 'heng',
    'hong', 'hou', 'hu', 'hua', 'huai', 'huan', 'huang', 'hui', 'hun', 'huo',
    'ji', 'jia', 'jian', 'jiang', 'jiao', 'jie', 'jin', 'jing', 'jiong', 'jiu', 'ju', 'juan', 'jue', 'jun',
    'ka', 'kai', 'kan', 'kang', 'kao', 'ke', 'kei', 'ken', 'keng',
    'kong', 'kou', 'ku', 'kua', 'kuai', 'kuan', 'kuang', 'kui', 'kun', 'kuo',
    'la', 'lai', 'lan', 'lang', 'lao', 'le', 'lei', 'leng',
    'li', 'lia', 'lian', 'liang', 'liao', 'lie', 'lin', 'ling', 'liu', 'long', 'lou',
    'lu', 'luan', 'lue', 'lun', 'luo', 'lv', 'lve', 'lvn', 'lü', 'lüe', 'lün',
    'ma', 'mai', 'man', 'mang', 'mao', 'me', 'mei', 'men', 'meng',
    'mi', 'mian', 'miao', 'mie', 'min', 'ming', 'miu', 'mo', 'mou', 'mu',
    'na', 'nai', 'nan', 'nang', 'nao', 'ne', 'nei', 'nen', 'neng',
    'ni', 'nia', 'nian', 'niang', 'niao', 'nie', 'nin', 'ning', 'niu',
    'nong', 'nou', 'nu', 'nuan', 'nue', 'nun', 'nuo', 'nv', 'nve', 'nü', 'nüe', 'ou',
    'pa', 'pai', 'pan', 'pang', 'pao', 'pei', 'pen', 'peng',
    'pi', 'pian', 'piao', 'pie', 'pin', 'ping', 'po', 'pou', 'pu',
    'qi', 'qia', 'qian', 'qiang', 'qiao', 'qie',
    'qin', 'qing', 'qiong', 'qiu', 'qu', 'quan', 'que', 'qun',
    'ran', 'rang', 'rao', 're', 'ren', 'reng', 'ri', 'rong', 'rou',
    'ru', 'rua', 'ruan', 'rui', 'run', 'ruo',
    'sa', 'sai', 'san', 'sang', 'sao', 'se', 'sei', 'sen', 'seng',
    'sha', 'shai', 'shan', 'shang', 'shao', 'she', 'shei', 'shen', 'sheng', 'shi',
    'shong', 'shou', 'shu', 'shua', 'shuai', 'shuan', 'shuang', 'shui', 'shun', 'shuo',
    'si', 'song', 'sou', 'su', 'suan', 'sui', 'sun', 'suo',
    'ta', 'tai', 'tan', 'tang', 'tao', 'te', 'tei', 'teng',
    'ti', 'tian', 'tiao', 'tie', 'ting', 'tong', 'tou',
    'tu', 'tuan', 'tui', 'tun', 'tuo',
    'wa', 'wai', 'wan', 'wang', 'wei', 'wen', 'weng', 'wo', 'wu',
    'xi', 'xia', 'xian', 'xiang', 'xiao', 'xie', 'xin', 'xing', 'xiong', 'xiu', 'xu', 'xuan', 'xue', 'xun',
    'ya', 'yai', 'yan', 'yang', 'yao', 'ye', 'yi', 'yin', 'ying',
    'yo', 'yong', 'you', 'yu', 'yuan', 'yue', 'yun',
    'za', 'zai', 'zan', 'zang', 'zao', 'ze', 'zei', 'zen', 'zeng',
    'zha', 'zhai', 'zhan', 'zhang', 'zhao', 'zhe', 'zhei', 'zhen', 'zheng',
    'zhi', 'zhong', 'zhou', 'zhu', 'zhua', 'zhuai', 'zhuan', 'zhuang', 'zhui', 'zhun', 'zhuo',
    'zi', 'zong', 'zou', 'zu', 'zuan', 'zui', 'zun', 'zuo', 'ê'
]

class PinyinSplit(NamedTuple):
    result: Optional[List[List[str]]]
    error_reason: Optional[str]

class PinyinSplitter():
    def __init__(self):
        self.trie = CharTrie()
        for final in finals_list:
            self.trie[final] = len(final)

    def _get_non_display_character(self, c: str) -> Optional[str]:
        for vowel_dict in vowels_by_tone.values():
            if c in vowel_dict:
                return vowel_dict[c]
        return c

    def split(self, pinyin: str, expected_output_length: Optional[int]) -> PinyinSplit:
        if not is_display_form(pinyin):
            return PinyinSplit(result=[], error_reason="pinyin not in display form")
        non_display_characters = [ self._get_non_display_character(c) for c in pinyin.lower() ]
        split_results = self._do_split("".join(non_display_characters))
        split_results_in_display_form = [
            self._return_result_to_display_form(pinyin, r) for r in split_results
        ]
        if expected_output_length is None:
            return PinyinSplit(result=split_results_in_display_form, error_reason=None)
        validated_results = [ r for r in split_results_in_display_form if len(r) == expected_output_length ]
        if not validated_results:
            return PinyinSplit(result=[], error_reason="No results found for split")
        return PinyinSplit(result=validated_results, error_reason=None)

    def _do_split(self, pinyin: str) -> List[List[str]]:
        split_list = []
        results = []
        if pinyin:
            split_list.append((pinyin, []))
        while split_list:
            pair = split_list.pop()
            pinyin = pair[0]
            words = pair[1]
            matches = self.trie.prefixes(pinyin)
            for match in matches:
                n = match[1]
                word = pinyin[:n]
                tail = pinyin[n:]
                new_words = copy.deepcopy(words) + [word]
                if tail:
                    split_list.append((tail, new_words))
                else:
                    results.append(new_words)
        return results

    def _return_result_to_display_form(self, original_pinyin: str, results: List[str]) -> List[str]:
        out = []
        pinyin_idx = 0
        for r in results:
            out.append(original_pinyin[pinyin_idx:pinyin_idx+len(r)])
            pinyin_idx += len(r)
        return out
