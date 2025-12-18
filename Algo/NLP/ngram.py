from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from NLP.tokenizer import tokenize

BigramCounts = Dict[str, Dict[str, int]]
UnigramCounts = Dict[str, int]

def _words_from_text(text: str) -> List[str]:
    return [t.text.lower() for t in tokenize(text)]

def train_ngram_model_from_text(text: str) -> tuple[BigramCounts, UnigramCounts]:
    words = _words_from_text(text)

    bigrams: BigramCounts = defaultdict(lambda: defaultdict(int))
    unigrams: UnigramCounts = defaultdict(int)

    for w in words:
        if len(w) >= 2:
            unigrams[w] += 1

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        if len(w1) < 2 or len(w2) < 2:
            continue
        bigrams[w1][w2] += 1

    return {k: dict(v) for k, v in bigrams.items()}, dict(unigrams)

def train_ngram_model_from_file(path: Path) -> tuple[BigramCounts, UnigramCounts]:
    if not path.exists():
        return {}, {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    return train_ngram_model_from_text(text)

def predict_next_words(context_word: str, bigrams: BigramCounts, k: int = 5) -> List[str]:
    w = context_word.lower()
    nexts = bigrams.get(w)
    if not nexts:
        return []
    return [w2 for w2, _ in sorted(nexts.items(), key=lambda x: x[1], reverse=True)[:k]]

def predict_completions(prefix: str, unigrams: UnigramCounts, k: int = 5) -> List[str]:
    p = prefix.lower()
    if len(p) < 2:
        return []
    candidates = [(w, c) for w, c in unigrams.items() if w.startswith(p) and w != p]
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [w for w, _ in candidates[:k]]
