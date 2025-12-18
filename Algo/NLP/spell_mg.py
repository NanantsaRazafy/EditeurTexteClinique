from __future__ import annotations
from rapidfuzz import process, fuzz

def suggest_mg(word: str, lexicon_list: list[str], limit: int = 5) -> list[str]:
    w = word.lower().strip()
    if len(w) < 2:
        return []

    # petit filtre pour aller vite
    first = w[0]
    candidates = [x for x in lexicon_list if len(x) >= 3 and x[0] == first and abs(len(x) - len(w)) <= 2]
    if not candidates:
        candidates = lexicon_list

    matches = process.extract(w, candidates, scorer=fuzz.WRatio, limit=limit * 5)
    out = [m for (m, score, _idx) in matches if score >= 75]
    return out[:limit]
