from __future__ import annotations
from pathlib import Path
import re

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
from functools import lru_cache
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parents[2]

RULES_PATH = BASE_DIR / "Data" / "rules_sample.json"
RULES = load_rules(RULES_PATH)

CORPUS_PATH = BASE_DIR / "Data" / "corpus_fr.txt"
BIGRAMS_FR, UNIGRAMS_FR = train_ngram_model_from_file(CORPUS_PATH)
BASE_DIR = Path(__file__).resolve().parents[2]

LEXICON_MG_PATH = BASE_DIR / "Data" / "clean" / "lexicon.json"
CORPUS_MG_PATH  = BASE_DIR / "Data" / "clean" / "corpus_clean.txt"


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

STOPWORDS_MG = {
    "ny", "dia", "ilay"
}

WORD_END_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ’']$")

def _is_typing_a_word(text: str, tokens) -> bool:
    if not text or not tokens:
        return False
    if not WORD_END_RE.search(text[-1]):
        return False
    return tokens[-1].end == len(text)

def _last_non_stopword(tokens) -> str | None:
    for t in reversed(tokens):
        w = t.text.lower()
        if len(w) < 2:
            continue
        if w in STOPWORDS_FR:
            continue
        return t.text
    return None

def analyze(text: str, lang: str = "fr") -> dict:
    issues = []
    issues.extend(apply_text_rules(text, RULES))

    tokens = tokenize(text)

    # init une seule fois
    next_word = []
    autocomplete = {"mode": "none", "suggestions": []}
    dbg_mg = None

    # Spellcheck MG
    if lang == "mg":
        lex_set = _mg_lexicon_set()
        lex_list = _mg_lexicon_list()

        for t in tokens:
            w = t.text.lower()
            if len(w) <= 1:
                continue
            if w not in lex_set:
                issues.append({
                    "start": t.start,
                    "end": t.end,
                    "word": t.text,
                    "type": "spell",
                    "severity": "warn",
                    "message": "Mot inconnu (MG)",
                    "suggestions": suggest_mg(t.text, lex_list, limit=5)
                })

        # Autocomplete MG
        if tokens:
            bigrams, unigrams = _mg_ngram_model()
            dbg_mg = {"bigrams": len(bigrams), "unigrams": len(unigrams)}

            if _is_typing_a_word(text, tokens):
                prefix = tokens[-1].text
                sugg = predict_completions(prefix, unigrams, k=5)
                autocomplete = {"mode": "completion", "suggestions": sugg}
                next_word = sugg
            else:
                context = tokens[-1].text
                sugg = predict_next_words(context, bigrams, k=5)
                autocomplete = {"mode": "next", "suggestions": sugg}
                next_word = sugg

    # Spellcheck FR
    elif lang == "fr":
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
                prefix = tokens[-1].text
                sugg = predict_completions(prefix, UNIGRAMS_FR, k=5)
                autocomplete = {"mode": "completion", "suggestions": sugg}
                next_word = sugg
            else:
                context = _last_non_stopword(tokens)
                if context:
                    sugg = predict_next_words(context, BIGRAMS_FR, k=5)
                    autocomplete = {"mode": "next", "suggestions": sugg}
                    next_word = sugg

    return {
        "issues": issues,
        "next_word": next_word,
        "autocomplete": autocomplete,
        "debug": {"lang": lang, "tokens": len(tokens), "mg_model": dbg_mg}
    }

