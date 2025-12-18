import json
import re

# Configuration des chemins selon votre structure de fichiers
INPUT_FILE = "../clean/corpus_clean.txt"
OUTPUT_LEXICON = "../clean/lexicon.json"
OUTPUT_LEMMAS = "../clean/lemmas.json"

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
        r'[bcdfghjklpqrstvwxyz]{3,}',    # Pas de clusters de 3 consonnes (ex: str)
        r'[^aeiouyàâôîùûéèç]$',           # Obligation de finir par une voyelle
        r'[qvwx]'                         # Lettres absentes du malgache standard (hors emprunts)
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, word):
            return False
    return True

# --- 2. LEMMATISATION RAFFINÉE ---
# Liste étendue pour protéger les entités nommées et les racines
PROTECTED_WORDS = {
    "madagasikara", "antananarivo", "antsiranana", "toamasina", 
    "fianarantsoa", "mahajanga", "toliara", "manakara", "ambositra",
    "ambatondrazaka", "ambalavao", "morondava", "antsirabe", "mananjary"
}

def lemmatize_word(word):
    """
    Réduit le mot à sa racine en gérant les affixes et la phonétique.
    """
    if word in PROTECTED_WORDS or len(word) <= 3:
        return word

    lemma = word
    # Préfixes et suffixes courants (ordre décroissant de longueur)
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
    # En malgache, un 'i' final en milieu de mot redevient souvent 'y' en fin de mot.
    if lemma.endswith('i'):
        lemma = lemma[:-1] + 'y'
    
    # Gestion spécifique des racines se terminant par une consonne après désaffixation
    # (Ex: fitovizana -> toviz -> tovy)
    if not re.search(r'[aeiouy]$', lemma):
        lemma += 'y'

    # Gestion du redoublement
    mid = len(lemma) // 2
    if len(lemma) >= 4 and lemma[:mid] == lemma[mid:]:
        lemma = lemma[:mid]

    return lemma

# --- 3. PIPELINE DE TRAITEMENT ---
def run_pipeline():
    try:
        # 1. Lecture
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            words = f.read().split()

        # 2. Filtrage et Lexique
        unique_words = sorted(set(w for w in words if is_valid_malagasy(w)))
        
        with open(OUTPUT_LEXICON, "w", encoding="utf-8") as f:
            json.dump(unique_words, f, ensure_ascii=False, indent=2)

        # 3. Lemmatisation
        lemmas_dict = {word: lemmatize_word(word) for word in unique_words}
        
        with open(OUTPUT_LEMMAS, "w", encoding="utf-8") as f:
            json.dump(lemmas_dict, f, ensure_ascii=False, indent=2)

        print(f"✔ Pipeline terminé avec succès !")
        print(f"   - Mots filtrés : {len(unique_words)}")
        print(f"   - Lemmes uniques : {len(set(lemmas_dict.values()))}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {INPUT_FILE} est introuvable.")

if __name__ == "__main__":
    run_pipeline()