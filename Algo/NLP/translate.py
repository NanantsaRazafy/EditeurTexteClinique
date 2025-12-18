from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

STRIP_RE = re.compile(r"^[^\wÀ-ÖØ-öø-ÿ’']+|[^\wÀ-ÖØ-öø-ÿ’']+$")

def normalize_word(w: str) -> str:
    w = w.strip()
    w = STRIP_RE.sub("", w)
    return w.lower()

def load_dictionary_csv(path: Path) -> Dict[str, List[str]]:
    """
    Charge un CSV mg,fr et retourne:
    { "salama": ["bonjour"], "razana": ["ancêtre"] }
    Supporte plusieurs traductions par mot (si plusieurs lignes).
    """
    if not path.exists():
        return {}

    mapping: Dict[str, List[str]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mg = normalize_word(row.get("mg", "") or "")
            fr = (row.get("fr", "") or "").strip()
            if not mg or not fr:
                continue
            mapping.setdefault(mg, [])
            if fr not in mapping[mg]:
                mapping[mg].append(fr)
    return mapping

def lookup(word: str, dictionary: Dict[str, List[str]]) -> Dict:
    raw = word
    w = normalize_word(word)

    translations = dictionary.get(w, [])
    return {
        "query": raw,
        "normalized": w,
        "found": len(translations) > 0,
        "translations": translations
    }
