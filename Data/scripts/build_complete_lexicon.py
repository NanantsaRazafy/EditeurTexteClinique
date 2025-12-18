import json
import re
import os

# Configuration des fichiers (Liste de sources)
INPUT_FILES = ["../clean/bible_clean_complete.json", "../clean/corpus_clean.txt"]
OUTPUT_LEXICON_JSON = "../clean/lexicon.json"
OUTPUT_LEMMAS_JSON = "../clean/lemmas_complete.json"

# Nouvelles sorties TXT
OUTPUT_LEXICON_TXT = "../clean/lexicon.txt"
OUTPUT_LEMMAS_TXT = "../clean/lemmas_complete.txt"

# --- 1. VALIDATION ---
def is_valid_malagasy(word):
    if len(word) < 2: return False
    # Nettoyage des caractères non alphabétiques résiduels
    word = re.sub(r'[^a-zàâôîùûéèç]', '', word.lower())
    if len(word) < 2: return False
    
    invalid_patterns = [
        r'nb|mk|dt|bp|sz|kg|pd|tj|gv', 
        r'[bcdfghjklpqrstvwxyz]{3,}', 
        r'[^aeiouyàâôîùûéèç]$', 
        r'[qvwx]'
    ]
    for pattern in invalid_patterns:
        if re.search(pattern, word): return False
    return True

# --- 2. LEMMATISATION AVANCÉE (Avec Infixes) ---
def advanced_lemmatize(word):
    PROTECTED_WORDS = {"madagasikara", "jesosy", "kristy", "isiraely", "andriamanitra"}
    word = word.lower()
    if word in PROTECTED_WORDS or len(word) <= 3:
        return word

    lemma = word

    # A. Infixes (-in-, -om-)
    for inf in ['in', 'om']:
        match = re.match(r'^([^aeiouy])' + inf + r'([aeiouy].*)', lemma)
        if match:
            lemma = match.group(1) + match.group(2)
            break

    # B. Affixes standards
    prefixes = ['mampy', 'mamp', 'manan', 'mana', 'man', 'mi', 'famp', 'fan', 'fi', 'ha']
    suffixes = ['inareo', 'anareo', 'tsika', 'ina', 'ana', 'ny', 'na', 'ko']

    for p in prefixes:
        if lemma.startswith(p) and len(lemma) > len(p) + 2:
            lemma = lemma[len(p):]; break
    for s in suffixes:
        if lemma.endswith(s) and len(lemma) > len(s) + 2:
            lemma = lemma[:-len(s)]; break

    # C. Phonétique & Redoublement
    if lemma.endswith('i'): lemma = lemma[:-1] + 'y'
    if not re.search(r'[aeiouyàâôîùûéèç]$', lemma): lemma += 'y'
    
    mid = len(lemma) // 2
    if len(lemma) >= 4 and lemma[:mid] == lemma[mid:]:
        lemma = lemma[:mid]

    return lemma

# --- 3. PIPELINE DE TRAITEMENT ---
def run_pipeline():
    all_words = []

    for file_path in INPUT_FILES:
        if not os.path.exists(file_path):
            print(f"⚠ Fichier ignoré (introuvable) : {file_path}")
            continue
        
        print(f"Traitement de : {file_path}...")
        
        if file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                def extract_from_dict(d):
                    for v in d.values():
                        if isinstance(v, dict): extract_from_dict(v)
                        else: all_words.extend(v.split())
                extract_from_dict(data)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                all_words.extend(f.read().split())

    # --- Nettoyage et Unification ---
    unique_words = sorted(set(w.lower().strip('.,!?:;()[]"') for w in all_words if is_valid_malagasy(w)))
    
    # --- SAUVEGARDE LEXIQUE ---
    # JSON
    with open(OUTPUT_LEXICON_JSON, "w", encoding="utf-8") as f:
        json.dump(unique_words, f, ensure_ascii=False, indent=2)
    # TXT
    with open(OUTPUT_LEXICON_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_words))

    # --- SAUVEGARDE LEMMES ---
    lemmas_dict = {word: advanced_lemmatize(word) for word in unique_words}
    # JSON
    with open(OUTPUT_LEMMAS_JSON, "w", encoding="utf-8") as f:
        json.dump(lemmas_dict, f, ensure_ascii=False, indent=2)
    # TXT (Format: mot_original -> lemme)
    with open(OUTPUT_LEMMAS_TXT, "w", encoding="utf-8") as f:
        for word, lemma in lemmas_dict.items():
            f.write(f"{word} -> {lemma}\n")

    print(f"\n✔ Terminé !")
    print(f"Lexique : {len(unique_words)} mots (sauvegardé en .json et .txt)")
    print(f"Lemmes  : {len(set(lemmas_dict.values()))} racines (sauvegardé en .json et .txt)")

if __name__ == "__main__":
    run_pipeline()