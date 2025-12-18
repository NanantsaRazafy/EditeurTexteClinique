import json
import re

# Chemins des fichiers
INPUT_JSON = "../clean/jaona_clean.json"
OUTPUT_LEXICON = "../clean/lexic.json"
OUTPUT_LEMMAS = "../clean/lemmas1.json"

# --- 1. VALIDATION PAR RÈGLES (REGEX) ---
def is_valid_malagasy(word):
    """
    Utilise des expressions régulières pour filtrer les mots non-malgaches.
    """
    if len(word) < 2:
        return False
    
    # Règles basées sur la phonotactique malgache
    invalid_patterns = [
        r'nb|mk|dt|bp|sz|kg|pd|tj|gv',    # Combinaisons de consonnes impossibles
        r'[bcdfghjklpqrstvwxyz]{3,}',    # Pas de clusters de 3 consonnes
        r'[^aeiouyàâôîùûéèç]$',           # Obligation de finir par une voyelle
        r'[qvwx]'                         # Lettres absentes du malgache standard
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, word):
            return False
    return True

# --- 2. LEMMATISATION RAFFINÉE ---
PROTECTED_WORDS = {
    "madagasikara", "antananarivo", "antsiranana", "toamasina", 
    "fianarantsoa", "mahajanga", "toliara", "manakara", "ambositra",
    "ambatondrazaka", "ambalavao", "morondava", "antsirabe", "mananjary",
    "jesosy", "kristy" # Ajout de noms bibliques protégés
}

def lemmatize_word(word):
    """
    Réduit le mot à sa racine en gérant les affixes et la phonétique.
    """
    if word in PROTECTED_WORDS or len(word) <= 3:
        return word

    lemma = word
    prefixes = ['mampy', 'mamp', 'manan', 'mana', 'man', 'mi', 'famp', 'fan', 'fi', 'ha']
    suffixes = ['ina', 'ana', 'ny', 'na']

    # Désaffixation
    for p in prefixes:
        if lemma.startswith(p) and len(lemma) > len(p) + 2:
            lemma = lemma[len(p):]
            break
            
    for s in suffixes:
        if lemma.endswith(s) and len(lemma) > len(s) + 2:
            lemma = lemma[:-len(s)]
            break

    # Règle de transformation phonétique
    if lemma.endswith('i'):
        lemma = lemma[:-1] + 'y'
    
    if not re.search(r'[aeiouy]$', lemma):
        lemma += 'y'

    # Gestion du redoublement
    mid = len(lemma) // 2
    if len(lemma) >= 4 and lemma[:mid] == lemma[mid:]:
        lemma = lemma[:mid]

    return lemma

# --- 3. PIPELINE DE TRAITEMENT POUR JSON ---
def run_pipeline():
    try:
        # 1. Lecture du JSON nettoyé
        with open(INPUT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extraction de tous les mots du texte
        all_words = []
        for chapter_key, verses in data.items():
            if chapter_key == "meta": continue
            for verse_num, text in verses.items():
                # On sépare les mots par les espaces
                all_words.extend(text.split())

        # 2. Filtrage et Lexique
        # On garde les mots uniques valides selon la phonotactique malgache
        unique_words = sorted(set(w for w in all_words if is_valid_malagasy(w)))
        
        with open(OUTPUT_LEXICON, "w", encoding="utf-8") as f:
            json.dump(unique_words, f, ensure_ascii=False, indent=2)

        # 3. Lemmatisation
        # Création du dictionnaire mot -> racine
        lemmas_dict = {word: lemmatize_word(word) for word in unique_words}
        
        with open(OUTPUT_LEMMAS, "w", encoding="utf-8") as f:
            json.dump(lemmas_dict, f, ensure_ascii=False, indent=2)

        print(f"✔ Lexique généré avec succès !")
        print(f"   - Mots extraits du JSON : {len(all_words)}")
        print(f"   - Mots uniques filtrés : {len(unique_words)}")
        print(f"   - Racines (lemmes) identifiées : {len(set(lemmas_dict.values()))}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {INPUT_JSON} est introuvable.")

if __name__ == "__main__":
    run_pipeline()