import re

def ensure_normalized_hanzi(hanzi: str) -> str:
    without_spaces = "".join(hanzi.split(" "))
    return (
        re.sub(
            r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+",
            "", without_spaces)
    )
