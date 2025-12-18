import re

INPUT_FILE = "../raw/wiki_raw.txt"
OUTPUT_FILE = "../clean/corpus_clean.txt"

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)          # supprimer chiffres
    text = re.sub(r"[^\w\sàâôîùûéèç]", "", text)
    text = re.sub(r"_", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

with open(INPUT_FILE, encoding="utf-8") as f:
    raw_text = f.read()

clean_text = clean_text(raw_text)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(clean_text)

print("✔ Nettoyage terminé")
print("Taille corpus :", len(clean_text), "caractères")
