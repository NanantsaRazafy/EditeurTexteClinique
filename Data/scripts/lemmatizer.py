import json
import re

# Chemins
INPUT_LEXICON = "../clean/lexicon.json"
OUTPUT_LEMMAS = "../clean/lemmas.json"

# Mots à ne pas toucher (Noms propres, etc.)
PROTECTED_WORDS = {
    "madagasikara", "antananarivo", "antsiranana", "toamasina", 
    "fianarantsoa", "mahajanga", "toliara", "manakara", "ambositra",
    "ambatondrazaka", "ambalavao", "morondava", "antsirabe"
}

def lemmatize_malagasy(word):
    if word in PROTECTED_WORDS or len(word) <= 3:
        return word

    lemma = word
    # 1. Suppression des affixes (du plus long au plus court)
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

    # 2. Règle d'or : Correction de la finale
    # Si finit par 'i', devient 'y' (ex: fotsi -> fotsy)
    if lemma.endswith('i'):
        lemma = lemma[:-1] + 'y'
    
    # Si finit par une consonne, on ajoute 'a' ou 'y' selon la phonétique 
    # (Ici 'y' est la solution la plus commune pour les racines)
    if not re.search(r'[aeiouyàâôîùûéèç]$', lemma):
        lemma += 'y'

    return lemma

# --- Exécution ---
with open(INPUT_LEXICON, "r", encoding="utf-8") as f:
    lexicon = json.load(f)

lemmatized_dict = {word: lemmatize_malagasy(word) for word in lexicon}

with open(OUTPUT_LEMMAS, "w", encoding="utf-8") as f:
    json.dump(lemmatized_dict, f, ensure_ascii=False, indent=2)

print(f"✔ Lemmatisation terminée pour {len(lemmatized_dict)} mots.")
# Vérification des exemples problématiques
test_cases = ["mianatra", "milalao", "mijery", "fotsy", "ravina", "fitovizana",]
# Test direct de la fonction (indépendant du lexique)
for t in test_cases:
    resultat = lemmatize_malagasy(t)
    print(f"Test direct : {t} -> {resultat}")
        