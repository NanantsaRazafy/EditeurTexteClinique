import json
import re
import os

# Configuration des fichiers (Liste de sources)
INPUT_FILES = ["../clean/bible_clean_complete.json", "../clean/corpus_clean.txt"]
OUTPUT_LEXICON = "../clean/lexicon.json"
OUTPUT_LEMMAS = "../clean/lemmas_complete.json"

# --- 1. VALIDATION ---
def is_valid_malagasy(word):
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
    if word.lower() in PROTECTED_WORDS or len(word) <= 3:
        return word.lower()

    lemma = word.lower()

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
        
        # Cas 1 : Si c'est le JSON de la Bible
        if file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # On extrait récursivement les textes du dictionnaire
                def extract_from_dict(d):
                    for v in d.values():
                        if isinstance(v, dict): extract_from_dict(v)
                        else: all_words.extend(v.split())
                extract_from_dict(data)
        
        # Cas 2 : Si c'est le corpus texte brut
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                all_words.extend(f.read().split())

    # Filtrage et Sauvegarde
    unique_words = sorted(set(w for w in all_words if is_valid_malagasy(w)))
    
    with open(OUTPUT_LEXICON, "w", encoding="utf-8") as f:
        json.dump(unique_words, f, ensure_ascii=False, indent=2)

    lemmas_dict = {word: advanced_lemmatize(word) for word in unique_words}
    with open(OUTPUT_LEMMAS, "w", encoding="utf-8") as f:
        json.dump(lemmas_dict, f, ensure_ascii=False, indent=2)

    print(f"\n✔ Terminé ! Lexique : {len(unique_words)} mots. Lemmes : {len(set(lemmas_dict.values()))}")

if __name__ == "__main__":
    run_pipeline()