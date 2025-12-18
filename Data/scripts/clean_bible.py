import json
import re
import os

# Configuration
INPUT_FILES = ["../clean/1-jaona.json", "../clean/2-jaona.json", "../clean/1-petera.json"] 
OUTPUT_FILE = "../clean/bible_clean_complete.json"

def clean_text(text):
    """Logique de nettoyage basée sur clean_corpus.py"""
    text = text.lower()
    text = re.sub(r"\d+", "", text)         # supprimer chiffres
    # On garde les lettres et les accents malgaches/français
    text = re.sub(r"[^\w\sàâôîùûéèç]", "", text)
    text = re.sub(r"_", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def process_bibles():
    merged_data = {}

    for file_name in INPUT_FILES:
        if not os.path.exists(file_name):
            print(f"⚠ Fichier {file_name} introuvable, sauté.")
            continue
            
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Utiliser le nom du livre comme clé principale (ex: "1-jaona")
            book_name = file_name.replace(".json", "")
            merged_data[book_name] = {}

            print(f"Processing: {book_name}...")

            for chapter_num, verses in data.items():
                # Ignorer les métadonnées pour ne garder que le texte biblique
                if chapter_num == "meta":
                    continue
                
                merged_data[book_name][chapter_num] = {}
                
                for verse_num, content in verses.items():
                    # Nettoyage du texte du verset
                    cleaned_content = clean_text(content)
                    merged_data[book_name][chapter_num][verse_num] = cleaned_content

    # Sauvegarde finale dans un seul fichier
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"\n✔ Fusion et nettoyage terminés !")
    print(f"Fichier de sortie : {OUTPUT_FILE}")

if __name__ == "__main__":
    process_bibles()