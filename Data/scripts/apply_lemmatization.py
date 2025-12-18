import json
import re

# Configuration
INPUT_LEXICON = "../clean/lexicon.json"
OUTPUT_LEMMAS = "../clean/lemmas_mapping.json"

def advanced_lemmatize(word):
    PROTECTED_WORDS = {"madagasikara", "antananarivo", "jesosy", "kristy", "isiraely", "andriamanitra"}
    if word.lower() in PROTECTED_WORDS or len(word) <= 3:
        return word.lower()

    lemma = word.lower()

    # --- 1. GESTION DES INFIXES (-in-, -om-) ---
    # Se placent après la première consonne : f-in-idy -> fidy
    infixes = ['in', 'om']
    for inf in infixes:
        match = re.match(r'^([^aeiouy])' + inf + r'([aeiouy].*)', lemma)
        if match:
            lemma = match.group(1) + match.group(2)
            break

    # --- 2. MUTATIONS DE CONSONNES (man-, fan-) ---
    if re.match(r'^[mnf]an', lemma) and len(lemma) > 5:
        remnant = lemma[3:]
        # Restauration de consonne (ex: manoratra -> soratra)
        if remnant.startswith(('o', 'a', 'i')):
            if remnant.startswith('ora'): lemma = "s" + remnant 
            else: lemma = remnant
        else:
            lemma = remnant

    # --- 3. PRÉFIXES ET SUFFIXES ÉTENDUS ---
    prefixes = ['mampy', 'mamp', 'manan', 'mana', 'mi', 'famp', 'fan', 'fi', 'ha']
    # Ajout de suffixes possessifs et pluriels complexes
    suffixes = ['inareo', 'anareo', 'tsika', 'ina', 'ana', 'ny', 'na', 'ko', 'ao']

    for p in prefixes:
        if lemma.startswith(p) and len(lemma) > len(p) + 2:
            lemma = lemma[len(p):]
            break
            
    for s in suffixes:
        if lemma.endswith(s) and len(lemma) > len(s) + 2:
            lemma = lemma[:-len(s)]
            break

    # --- 4. CORRECTIONS PHONÉTIQUES ET REDOUBLEMENT ---
    if lemma.endswith('i'):
        lemma = lemma[:-1] + 'y'
    
    if not re.search(r'[aeiouyàâôîùûéèç]$', lemma):
        lemma += 'y'

    # Gestion du redoublement (mandehandeha -> mandeha)
    mid = len(lemma) // 2
    if len(lemma) >= 4 and lemma[:mid] == lemma[mid:]:
        lemma = lemma[:mid]

    return lemma

def process_lexicon():
    try:
        with open(INPUT_LEXICON, "r", encoding="utf-8") as f:
            lexicon_list = json.load(f)
        
        lemmas_mapping = {word: advanced_lemmatize(word) for word in lexicon_list}

        with open(OUTPUT_LEMMAS, "w", encoding="utf-8") as f:
            json.dump(lemmas_mapping, f, ensure_ascii=False, indent=2)

        print(f"✔ Mapping généré avec succès dans {OUTPUT_LEMMAS}")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    process_lexicon()