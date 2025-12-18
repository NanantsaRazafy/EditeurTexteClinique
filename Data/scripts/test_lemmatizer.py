import re

def advanced_lemmatize(word):
    # Logique identique au script de traitement
    if len(word) <= 3: return word.lower()

    lemma = word.lower()

    # Infixes (-in-, -om-)
    for inf in ['in', 'om']:
        match = re.match(r'^([^aeiouy])' + inf + r'([aeiouy].*)', lemma)
        if match:
            lemma = match.group(1) + match.group(2)
            break

    # Préfixes & Mutations
    if re.match(r'^[mnf]an', lemma) and len(lemma) > 4:
        lemma = lemma[3:]
    
    prefixes = ['mampy', 'mamp', 'manan', 'mana', 'mi', 'famp', 'fan', 'fi', 'ha']
    suffixes = ['inareo', 'anareo', 'tsika', 'ina', 'ana', 'ny', 'na', 'ko']

    for p in prefixes:
        if lemma.startswith(p) and len(lemma) > len(p) + 2:
            lemma = lemma[len(p):]
            break
    for s in suffixes:
        if lemma.endswith(s) and len(lemma) > len(s) + 2:
            lemma = lemma[:-len(s)]
            break

    if lemma.endswith('i'): lemma = lemma[:-1] + 'y'
    if not re.search(r'[aeiouyàâôîùûéèç]$', lemma): lemma += 'y'
    
    mid = len(lemma) // 2
    if len(lemma) >= 4 and lemma[:mid] == lemma[mid:]: lemma = lemma[:mid]

    return lemma

print("--- TESTEUR DE LEMMATISATION (Avec Infixes) ---")
print("Exemples : 'finidy' -> 'fidy', 'homana' -> 'hana'")

while True:
    test = input("\nEntrez un mot (ou 'q') : ").strip()
    if test.lower() == 'q': break
    print(f"Racine : {advanced_lemmatize(test)}")