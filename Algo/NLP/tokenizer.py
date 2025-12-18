import re
from dataclasses import dataclass

WORD_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[’'][A-Za-zÀ-ÖØ-öø-ÿ]+)?(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+)*"
)

@dataclass(frozen=True)
class Token:
    text: str
    start: int
    end: int

def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    for m in WORD_RE.finditer(text):
        tokens.append(Token(text=m.group(0), start=m.start(), end=m.end()))
    return tokens
