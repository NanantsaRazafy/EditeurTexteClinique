from __future__ import annotations

from pathlib import Path
import re
from functools import lru_cache

from NLP.tokenizer import tokenize
from NLP.spell_fr import is_known_fr, suggest_fr
from NLP.lexicon_mg import load_lexicon_mg_json
from NLP.spell_mg import suggest_mg
from NLP.rules_engine import apply_text_rules, load_rules
from NLP.ngram import (
    train_ngram_model_from_file,
    predict_next_words,
    predict_completions
)

# ----------------------------
# Paths & resources
# ----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

RULES_PATH = BASE_DIR / "Data" / "rules_sample.json"
RULES = load_rules(RULES_PATH)

RULES_MG_PATH = BASE_DIR / "Data" / "regex" / "rules_mg.json"
RULES_MG = load_rules(RULES_MG_PATH)

CORPUS_FR_PATH = BASE_DIR / "Data" / "corpus_fr.txt"
BIGRAMS_FR, UNIGRAMS_FR = train_ngram_model_from_file(CORPUS_FR_PATH)

LEXICON_MG_PATH = BASE_DIR / "Data" / "clean" / "lexicon.json"
CORPUS_MG_PATH = BASE_DIR / "Data" / "clean" / "corpus_clean.txt"


@lru_cache(maxsize=1)
def _mg_lexicon_set() -> set[str]:
    return load_lexicon_mg_json(LEXICON_MG_PATH)


@lru_cache(maxsize=1)
def _mg_lexicon_list() -> list[str]:
    return sorted(list(_mg_lexicon_set()))


@lru_cache(maxsize=1)
def _mg_ngram_model():
    return train_ngram_model_from_file(CORPUS_MG_PATH)


STOPWORDS_FR = {
    "de", "des", "du", "la", "le", "les", "et", "en", "dans", "sur", "pour",
    "avec", "que", "qui", "au", "aux", "a", "à"
}

WORD_END_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ’']$")


def _is_typing_a_word(text: str, tokens) -> bool:
    if not text or not tokens:
        return False
    if not WORD_END_RE.search(text[-1]):
        return False
    return tokens[-1].end == len(text)


def _last_non_stopword_fr(tokens) -> str | None:
    for t in reversed(tokens):
        w = t.text.lower()
        if len(w) < 2:
            continue
        if w in STOPWORDS_FR:
            continue
        return t.text
    return None


def analyze(text: str, lang: str = "fr") -> dict:
    issues: list[dict] = []

    # règles communes (si tu en as)
    issues.extend(apply_text_rules(text, RULES))

    tokens = tokenize(text)

    # init une seule fois
    next_word: list[str] = []
    autocomplete = {"mode": "none", "suggestions": []}
    dbg_mg = None

    # Malagasy
    if lang == "mg":
        # 1) Règles regex MG en token-level
        for t in tokens:
            local_issues = apply_text_rules(t.text, RULES_MG)
            for iss in local_issues:
                iss["start"] = t.start + iss.get("start", 0)
                iss["end"] = t.start + iss.get("end", len(t.text))
                iss["word"] = t.text
                iss["scope"] = "token"
            issues.extend(local_issues)

        # 2) Construire les spans qui ont déjà une rule WARN
        rule_warn_spans = {
            (iss["start"], iss["end"])
            for iss in issues
            if iss.get("type") == "rule" and iss.get("severity") == "warn"
        }

        # 3) Spellcheck MG (downgrade si déjà rule warn)
        lex_set = _mg_lexicon_set()
        lex_list = _mg_lexicon_list()

        for t in tokens:
            w = t.text.lower()
            if len(w) <= 1:
                continue
            if w not in lex_set:
                sev = "warn"
                if (t.start, t.end) in rule_warn_spans:
                    sev = "info"

                issues.append({
                    "start": t.start,
                    "end": t.end,
                    "word": t.text,
                    "type": "spell",
                    "severity": sev,
                    "message": "Mot inconnu (MG)",
                    "suggestions": suggest_mg(t.text, lex_list, limit=5)
                })

        # 4) Autocomplete MG
        if tokens:
            bigrams, unigrams = _mg_ngram_model()
            dbg_mg = {"bigrams": len(bigrams), "unigrams": len(unigrams)}

            if _is_typing_a_word(text, tokens):
                prefix = tokens[-1].text.lower()
                sugg = predict_completions(prefix, unigrams, k=5)

                # fallback lexicon si ton corpus est petit
                if not sugg:
                    # lex_list est triée: on propose les premiers qui matchent le préfixe
                    p = prefix
                    tmp = []
                    for w in lex_list:
                        if w.startswith(p):
                            tmp.append(w)
                            if len(tmp) >= 5:
                                break
                    sugg = tmp

                autocomplete = {"mode": "completion", "suggestions": sugg}
                next_word = sugg
            else:
                context = tokens[-1].text.lower()
                sugg = predict_next_words(context, bigrams, k=5)
                autocomplete = {"mode": "next", "suggestions": sugg}
                next_word = sugg

    # Français
    elif lang == "fr":
        # Spellcheck FR
        for t in tokens:
            if not is_known_fr(t.text):
                issues.append({
                    "start": t.start,
                    "end": t.end,
                    "word": t.text,
                    "type": "spell",
                    "severity": "warn",
                    "message": "Mot probablement incorrect / inconnu (FR)",
                    "suggestions": suggest_fr(t.text, limit=5)
                })

        # Autocomplete FR
        if tokens:
            if _is_typing_a_word(text, tokens):
                prefix = tokens[-1].text.lower()
                sugg = predict_completions(prefix, UNIGRAMS_FR, k=5)
                autocomplete = {"mode": "completion", "suggestions": sugg}
                next_word = sugg
            else:
                context = _last_non_stopword_fr(tokens)
                if context:
                    sugg = predict_next_words(context.lower(), BIGRAMS_FR, k=5)
                    autocomplete = {"mode": "next", "suggestions": sugg}
                    next_word = sugg

    return {
        "issues": issues,
        "next_word": next_word,
        "autocomplete": autocomplete,
        "debug": {"lang": lang, "tokens": len(tokens), "mg_model": dbg_mg}
    }
