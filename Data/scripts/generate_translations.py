import json
import time
from deep_translator import GoogleTranslator 

# Configuration
INPUT_LEMMAS = "../clean/lemmas_complete.json"
OUTPUT_TRANSLATIONS = "../clean/translations_mapping.json"

def translate_lexicon():
    try:
        # 1. Charger les lemmes (on traduit les racines car c'est le plus efficace)
        with open(INPUT_LEMMAS, "r", encoding="utf-8") as f:
            lemmas_dict = json.load(f)

        # Extraire uniquement les racines uniques pour économiser les appels API
        unique_roots = sorted(list(set(lemmas_dict.values())))
        print(f"Nombre de racines uniques à traduire : {len(unique_roots)}")

        translator = GoogleTranslator(source='mg', target='fr')
        translations = {}

        # 2. Traduction par lots (pour éviter les blocages)
        count = 0
        for root in unique_roots:
            try:
                # Traduction de la racine
                translated = translator.translate(root)
                translations[root] = translated
                count += 1
                
                if count % 10 == 0:
                    print(f"Traduit : {count}/{len(unique_roots)}...")
                
                # Petite pause pour respecter les limites de l'API gratuite
                time.sleep(0.1) 
            except Exception as e:
                print(f"Erreur sur le mot '{root}': {e}")
                translations[root] = "TODO" # Marqueur pour traduction manuelle

        # 3. Sauvegarder le dictionnaire de traduction
        with open(OUTPUT_TRANSLATIONS, "w", encoding="utf-8") as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)

        print(f"\n✔ Terminé ! Fichier de traduction créé : {OUTPUT_TRANSLATIONS}")

    except Exception as e:
        print(f"Erreur générale : {e}")

if __name__ == "__main__":
    translate_lexicon()