import json

# Chemins
INPUT_FILE = "../clean/corpus_clean.txt"
OUTPUT_FILE = "../clean/lexicon.json"

# Combinaisons interdites en malagasy
INVALID_COMBINATIONS = ["nb", "mk", "dt", "bp", "sz"]

# 1️⃣ Lecture du corpus
with open(INPUT_FILE, encoding="utf-8") as f:
    words = f.read().split()

# 2️⃣ Suppression des doublons
unique_words = set(words)

# 3️⃣ Filtrage linguistique malagasy
def is_valid_malagasy_word(word):
    if len(word) < 2:
        return False
    for combo in INVALID_COMBINATIONS:
        if combo in word:
            return False
    return True

lexicon = sorted(
    w for w in unique_words if is_valid_malagasy_word(w)
)

# 4️⃣ Sauvegarde
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(lexicon, f, ensure_ascii=False, indent=2)

print("✔ Lexique créé :", len(lexicon), "mots")
print("Exemples :", lexicon[:20])
