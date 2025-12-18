import json
import re

def clean_text(text):
    # Logique strictement identique à clean_corpus.py
    text = text.lower()
    text = re.sub(r"\d+", "", text)          # supprimer chiffres
    text = re.sub(r"[^\w\sàâôîùûéèç]", "", text) # supprimer ponctuation (sauf accents)
    text = re.sub(r"_", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Chargement du fichier JSON source
with open('../clean/1-jaona.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Parcours récursif pour nettoyer uniquement les valeurs de texte
for chapter_key in data:
    if chapter_key == "meta":
        continue
    
    chapter = data[chapter_key]
    for verse_key in chapter:
        # Application du nettoyage sur chaque verset
        original_text = chapter[verse_key]
        chapter[verse_key] = clean_text(original_text)

# Sauvegarde du nouveau fichier nettoyé
with open('../clean/jaona_clean.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✔ Nettoyage du JSON terminé avec succès.")