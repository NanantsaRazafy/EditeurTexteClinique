from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def load_lexicon_mg_json(path: Path) -> set[str]:
    
    if not path.exists():
        return set()

    data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    out: set[str] = set()

    def add(w: str):
        w = (w or "").strip().lower()
        if len(w) > 1:
            out.add(w)

    def walk(x: Any):
        if x is None:
            return
        if isinstance(x, str):
            add(x)
            return
        if isinstance(x, list):
            for item in x:
                walk(item)
            return
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(k, str):
                    add(k)
                if isinstance(v, dict):
                    for key in ("word", "lemma", "entry", "form"):
                        if key in v and isinstance(v[key], str):
                            add(v[key])
                walk(v)

    walk(data)
    return out
