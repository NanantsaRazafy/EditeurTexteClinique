from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

# === Chemins ===
# === Chemins ===
BASE_DIR = Path(__file__).resolve().parents[2]   # repo root
CORPUS_PATH = BASE_DIR / "Data" / "clean" / "corpus_clean.txt"

OUT_DIR = BASE_DIR / "Data" / "translate"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOP_WORDS_CSV = OUT_DIR / "top_words_mg.csv"
TODO_CSV = OUT_DIR / "todo_translate_mg_fr.csv"
SKELETON_JSON = OUT_DIR / "mg_fr_skeleton.json"

# === Paramètres ===
TOP_N = 200              # change à 500/1000/5000 si tu veux
MIN_LEN = 2               # ignore 1 lettre
MIN_FREQ = 2              # ignore les mots vus 1 seule fois (bruit)

# Stopwords MG (tu peux enrichir)
STOPWORDS_MG = {
    "ny", "dia", "ilay", "ary", "fa", "ka", "nefa", "noho", "izay",
    "ao", "amin", "an", "sy", "ho", "na", "efa", "tsy", "toa", "mbola"
}

# Tokenizer simple (lettres + apostrophes)
TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ’']+")

def normalize_token(t: str) -> str:
    return t.strip().lower()

def main() -> None:
    if not CORPUS_PATH.exists():
        raise FileNotFoundError(f"Corpus introuvable: {CORPUS_PATH}")

    counts = Counter()

    # Lecture streaming (ok même si gros fichier)
    with CORPUS_PATH.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for tok in TOKEN_RE.findall(line):
                w = normalize_token(tok)
                if len(w) < MIN_LEN:
                    continue
                if w in STOPWORDS_MG:
                    continue
                counts[w] += 1

    # Filtrer / trier
    items = [(w, c) for w, c in counts.items() if c >= MIN_FREQ]
    items.sort(key=lambda x: x[1], reverse=True)
    top = items[:TOP_N]

    # 1) CSV: top words
    with TOP_WORDS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mg", "freq"])
        writer.writerows(top)

    # 2) CSV: à traduire
    with TODO_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mg", "fr"])  # colonne fr vide à remplir
        for w, _c in top:
            writer.writerow([w, ""])

    # 3) JSON skeleton
    skeleton = {"mg_to_fr": {}}
    with SKELETON_JSON.open("w", encoding="utf-8") as f:
        json.dump(skeleton, f, ensure_ascii=False, indent=2)

    print("OK ✅")
    print("Top words CSV:", TOP_WORDS_CSV)
    print("TODO translate CSV:", TODO_CSV)
    print("Skeleton JSON:", SKELETON_JSON)

if __name__ == "__main__":
    main()
