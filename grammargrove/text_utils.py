import string
import re

def remove_punctuation(st: str) -> str:
    for punc in string.punctuation:
        st = st.replace(punc, "")
    return st


def remove_punctuation_from_hanzi(hanzi: str) -> str:
    without_spaces = "".join(hanzi.split(" "))
    return (
        re.sub(
            r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+",
            "", without_spaces)
    )


def has_hanzi(s: str) -> bool:
    return re.search(u'[\u4e00-\u9fff]', s) is not None

