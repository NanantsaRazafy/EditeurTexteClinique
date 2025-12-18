import json
import re

# Configuration des fichiers
INPUT_JSON = "../clean/bible_clean_complete.json"
OUTPUT_LEXICON = "../clean/lexicon_complete.json"
OUTPUT_LEMMAS = "../clean/lemmas_complete.json"

# --- 1. VALIDATION PAR RÈGLES (LOGIQUE DE BUILD_JSON_LEXICON.PY) ---
def is_valid_malagasy(word):
    """Filtre les mots selon la phonotactique malgache."""
    if len(word) < 2:
        return False
    
    invalid_patterns = [
        r'nb|mk|dt|bp|sz|kg|pd|tj|gv',    # Combinaisons impossibles
        r'[bcdfghjklpqrstvwxyz]{3,}',    # Pas de clusters de 3 consonnes
        r'[^aeiouyàâôîùûéèç]$',           # Doit finir par une voyelle
        r'[qvwx]'                         # Lettres exclues
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, word):
            return False
    return True

# --- 2. LEMMATISATION (LOGIQUE DE BUILD_JSON_LEXICON.PY) ---
PROTECTED_WORDS = {
    "madagasikara", "antananarivo", "jesosy", "kristy", "isiraely"
}

def lemmatize_word(word):
    """Réduit le mot à sa racine."""
    if word in PROTECTED_WORDS or len(word) <= 3:
        return word

    lemma = word
    prefixes = ['mampy', 'mamp', 'manan', 'mana', 'man', 'mi', 'famp', 'fan', 'fi', 'ha']
    suffixes = ['ina', 'ana', 'ny', 'na']

    for p in prefixes:
        if lemma.startswith(p) and len(lemma) > len(p) + 2:
            lemma = lemma[len(p):]
            break
            
    for s in suffixes:
        if lemma.endswith(s) and len(lemma) > len(s) + 2:
            lemma = lemma[:-len(s)]
            break

    if lemma.endswith('i'):
        lemma = lemma[:-1] + 'y'
    
    if not re.search(r'[aeiouy]$', lemma):
        lemma += 'y'

    return lemma

# --- 3. TRAITEMENT DU JSON MULTI-LIVRES ---
def run_pipeline():
    try:
        with open(INPUT_JSON, "r", encoding="utf-8") as f:
            bible_data = json.load(f)

        all_words = []
        
        # Parcours de la nouvelle structure : Livre -> Chapitre -> Verset
        for book_name, chapters in bible_data.items():
            print(f"Extraction des mots de : {book_name}")
            for chapter_num, verses in chapters.items():
                for verse_num, text in verses.items():
                    all_words.extend(text.split())

        # Filtrage des mots uniques
        unique_words = sorted(set(w for w in all_words if is_valid_malagasy(w)))
        
        # Sauvegarde du Lexique
        with open(OUTPUT_LEXICON, "w", encoding="utf-8") as f:
            json.dump(unique_words, f, ensure_ascii=False, indent=2)

        # Sauvegarde des Lemmes
        lemmas_dict = {word: lemmatize_word(word) for word in unique_words}
        with open(OUTPUT_LEMMAS, "w", encoding="utf-8") as f:
            json.dump(lemmas_dict, f, ensure_ascii=False, indent=2)

        print(f"\n✔ Analyse terminée !")
        print(f"   - Total mots traités : {len(all_words)}")
        print(f"   - Mots uniques (lexique) : {len(unique_words)}")
        print(f"   - Racines uniques : {len(set(lemmas_dict.values()))}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {INPUT_JSON} est introuvable.")

if __name__ == "__main__":
    run_pipeline()