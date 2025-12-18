from __future__ import annotations

from functools import lru_cache
from wordfreq import zipf_frequency, top_n_list
from rapidfuzz import process, fuzz

EXTRA_WORDS = [
    "pizza", "pizzas", "mange", "manger", "mangé", "mangeais", "mangeait"
]

def is_known_fr(word: str) -> bool:
    w = word.lower()
    if len(w) <= 1:
        return True
    return zipf_frequency(w, "fr") >= 2.0

@lru_cache(maxsize=1)
def _vocab_fr() -> list[str]:
    try:
        vocab = top_n_list("fr", 20000)  
    except Exception:
        vocab = []

    vocab = list(dict.fromkeys(EXTRA_WORDS + vocab))

    vocab = [w for w in vocab if len(w) >= 2]
    return vocab

def suggest_fr(word: str, limit: int = 5) -> list[str]:
    w = word.lower()
    vocab = _vocab_fr()

    matches = process.extract(w, vocab, scorer=fuzz.WRatio, limit=limit * 5)

    out: list[str] = []
    for m, score, _ in matches:
        if score < 75:
            continue
        if m[0] != w[0]:
            continue
        out.append(m)
        if len(out) >= limit:
            break
    return out
