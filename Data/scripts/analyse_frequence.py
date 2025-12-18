import json
from collections import Counter

# Chemins
CORPUS_FILE = "../clean/corpus_clean.txt"
LEMMAS_FILE = "../clean/lemmas.json"
OUTPUT_STATS = "../clean/stats_frequence.json"

def generate_stats():
    try:
        # 1. Charger le dictionnaire de lemmes {mot: racine}
        with open(LEMMAS_FILE, "r", encoding="utf-8") as f:
            lemmas_dict = json.load(f)

        # 2. Lire le corpus complet
        with open(CORPUS_FILE, "r", encoding="utf-8") as f:
            words = f.read().split()

        # 3. Transformer chaque mot du texte en son lemme
        # Si le mot n'est pas dans le dictionnaire (ex: mot filtré), on l'ignore
        lemmatized_text = [
            lemmas_dict[w] for w in words if w in lemmas_dict
        ]

        # 4. Compter les fréquences
        stats = Counter(lemmatized_text)

        # 5. Trier par les plus fréquents
        sorted_stats = dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))

        # 6. Sauvegarder les résultats
        with open(OUTPUT_STATS, "w", encoding="utf-8") as f:
            json.dump(sorted_stats, f, ensure_ascii=False, indent=2)

        print(f"✔ Analyse terminée sur {len(words)} mots.")
        print("\n--- Top 10 des concepts les plus fréquents ---")
        for i, (lemma, count) in enumerate(list(sorted_stats.items())[:10]):
            print(f"{i+1}. {lemma.ljust(15)} : {count} occurrences")

    except FileNotFoundError:
        print("Erreur : Assurez-vous d'avoir généré corpus_clean.txt et lemmas.json")

if __name__ == "__main__":
    generate_stats()