import json
from collections import Counter
from deep_translator import GoogleTranslator
import time

# Fichiers source
CORPUS_FILE = "../clean/corpus_clean.txt"
LEMMAS_FILE = "../clean/lemmas.json"

# Liste des mots outils à ignorer pour l'analyse
STOP_WORDS = {"ny", "sy", "dia", "no", "ary", "ho", "na", "ao", "any", "tao", "ireo", "izy", "ana", "koa", "izay", "eto"}

def generer_analyse_google():
    try:
        # 1. Chargement des données
        with open(LEMMAS_FILE, "r", encoding="utf-8") as f:
            lemmas_dict = json.load(f)
        with open(CORPUS_FILE, "r", encoding="utf-8") as f:
            tokens = f.read().split()

        # 2. Filtrage et comptage
        # On remplace chaque mot par son lemme s'il n'est pas dans la liste STOP_WORDS
        lemmatized_list = [
            lemmas_dict[w] for w in tokens 
            if w in lemmas_dict and lemmas_dict[w] not in STOP_WORDS
        ]
        top_items = Counter(lemmatized_list).most_common(15)

        # 3. Initialisation du traducteur (Malgache -> Français)
        translator = GoogleTranslator(source='mg', target='fr')

        print(f"\n--- Analyse Finale (Traduction via Google) ---")
        print(f"{'LEMME':<15} | {'FREQ':<5} | {'TRADUCTION'}")
        print("-" * 55)

        # 4. Traduction et affichage
        for lemma, freq in top_items:
            try:
                # Traduction du lemme unique
                trad = translator.translate(lemma)
                # Petit délai de sécurité pour éviter le blocage IP
                time.sleep(0.3) 
            except Exception as e:
                trad = f"[Erreur: {e}]"
            
            print(f"{lemma:<15} | {freq:<5} | {trad}")

    except Exception as e:
        print(f"Erreur système : {e}")

if __name__ == "__main__":
    generer_analyse_google()