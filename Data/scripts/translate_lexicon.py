import json
import time
import os
from deep_translator import GoogleTranslator

# Configuration
INPUT_LEMMAS = "../clean/lemmas_complete.json"
OUTPUT_TRANSLATION = "../clean/lexicon_translated.json"

def translate_lexicon():
    # Initialisation du traducteur (Malgache -> Français)
    translator = GoogleTranslator(source='mg', target='fr')
    
    try:
        # 1. Charger les lemmes
        if not os.path.exists(INPUT_LEMMAS):
            print(f"Erreur : Le fichier {INPUT_LEMMAS} est introuvable.")
            return

        with open(INPUT_LEMMAS, "r", encoding="utf-8") as f:
            lemmas_dict = json.load(f)

        # 2. Identifier les racines uniques
        unique_roots = sorted(list(set(lemmas_dict.values())))
        total = len(unique_roots)
        print(f"Nombre de racines uniques à traduire : {total}")

        translations = {}
        
        # 3. Traduction individuelle (plus stable)
        for index, root in enumerate(unique_roots, 1):
            if not root or root.strip() == "":
                continue
            
            try:
                # Traduction
                translated = translator.translate(root)
                translations[root] = translated
                
                # Affichage de la progression
                if index % 10 == 0:
                    print(f"Progression : {index}/{total} (Dernier : {root} -> {translated})")
                
                # Pause courte pour éviter d'être banni par Google
                time.sleep(0.3) 
                
            except Exception as e:
                print(f"Erreur sur '{root}': {e}")
                translations[root] = root  # Garder l'original en cas d'échec
                time.sleep(2) # Pause plus longue en cas d'erreur réseau

        # 4. Fusionner avec le lexique complet
        final_result = {}
        for word, root in lemmas_dict.items():
            final_result[word] = {
                "root": root,
                "translation_fr": translations.get(root, "Non traduit")
            }

        # 5. Sauvegarde finale
        with open(OUTPUT_TRANSLATION, "w", encoding="utf-8") as f:
            json.dump(final_result, f, ensure_ascii=False, indent=2)

        print(f"\n✔ Traduction terminée avec succès !")
        print(f"Fichier créé : {OUTPUT_TRANSLATION}")

    except Exception as e:
        print(f"Erreur critique : {e}")

if __name__ == "__main__":
    translate_lexicon()