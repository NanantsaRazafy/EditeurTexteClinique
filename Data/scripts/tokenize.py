with open("../clean/corpus_clean.txt", encoding="utf-8") as f:
    words = f.read().split()

print("Nombre de mots :", len(words))
print("Exemple :", words[:20])
