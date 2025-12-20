# **Rapport de Projet \- EDITEUR DE TEXTE AUGMENTE PAR L'IA POUR LE MALAGASY - SEVENFOLD**

## **Examen CLINIQUE - Intelligence Artificielle**

Réalisé au sein de ISPM - Madagascar (www.ispm-edu.com)

### **1\. Informations sur le Groupe**


#### Membre 1 : 
* nom : RAKOTOMANANA NOMENJANAHARY
* prénom(s) : Aina
* classe : ESIIA 5
* numéro : 01
* rôle : Frontend Developer - UI/UX Designer

#### Membre 2 : 
* nom : RAZAFINANTOANDRO
* prénom(s) : Antsasoa
* classe : IMTICIA 5
* numéro : 11
* rôle : Frontend Developer - UI/UX Designer

#### Membre 3 : 
* nom : HERIMAMPIONONA
* prénom(s) : Tahiry Mariano
* classe : ESIIA 5
* numéro : 12
* rôle : NLP Data spécialist (Web Scraping & Data collection)

#### Membre 4 : 
* nom : TIAHARISON 
* prénom(s) : Serge Eric
* classe : IMTICIA 5
* numéro : 13
* rôle : Symbolic AI Engineer (GLCIA)

#### Membre 5 : 
* nom : RABOANARY 
* prénom(s) : Kanto Faratiana Nicole
* classe : ESIIA 5
* numéro : 17
* rôle : NLP Engineer (Algorithms & APIs)

#### Membre 6 : 
* nom : RANDRIAMBOAVONJY
* prénom(s) : Rotsy Ny Aina Miotisoa Landô
* classe : ESIIA 5
* numéro : 20
* rôle : NLP Data spécialist (Web Scraping & Data collection)

#### Membre 7 : 
* nom : RANDRIARINIAINA
* prénom(s) : Andritiana Jordi
* classe : ESIIA 5
* numéro : 24
* rôle : AI Assistant Developer

### **2\. Documentation technique**

**Objectif** : Développer un éditeur de texte intelligent pour la langue malagasy, en contournant le manque de données numériques grâce à des approches hybrides (symboliques, algorithmiques et data-driven).

**Architecture Générale** :\
Frontend (Web)\
└─ Éditeur riche (Quill.js / CKEditor)\
↓ API REST\
Backend (Python)\
├─ NLP & règles linguistiques\
├─ Services IA\
└─ Accès aux corpus\
↓
Données\
├─ Lexiques\
├─ Corpus nettoyés\
└─ Ontologies

**Technologies principales** :
- **Frontend** : React, Quill.js / CKEditor  
- **Backend** : Python, FastAPI / Flask, NLTK, spaCy, RapidFuzz  
- **Scraping & Data** : Requests, BeautifulSoup, JSON
- **TTS** : gTTS  

#### Mots-clés :  
NLP, Scraping, TTS, NER, Chatbot

### **3\. Liste et brève description des fonctionnalités IA**

| Fonctionnalité | Description |
|----------------|------------|
| Correcteur orthographique | Vérifie l’orthographe malagasy via lexiques et distance de Levenshtein |
| Vérification à base de règles | Détecte les erreurs phonotactiques et morphologiques (`nb`, `mk`, etc.) |
| Lemmatisation | Retrouve la racine des mots malagasy en supprimant préfixes et suffixes |
| Autocomplétion / Next Word Prediction | Modèles N-grams / Markov pour prédire le mot suivant |
| Traduction mot-à-mot | Affichage des traductions via dictionnaire local ou APIs externes |
| Explorateur sémantique | Suggestions basées sur ontologie (ex: Fianakaviana, Sakafo) |
| Analyse de sentiment | Classification simple Positif/Négatif via lexique malagasy |
| Synthèse vocale (TTS) | Lecture du texte avec accent malagasy |
| Reconnaissance d’entités (NER) | Détection de villes, lieux, personnalités |
| Chatbot Assistant | Synonymes, conjugaisons, aide linguistique |


**🔗 Liens Utiles :**

- [**LIEN VERS LA VIDÉO DE PRÉSENTATION** (YouTube)](https://www.youtube.com/watch?v=xLPEdvkLBow)  


### **4\. Bibliographie**
- **Wikipedia Malagasy** – [mg.wikipedia.org](https://mg.wikipedia.org)  
- **tenymalagasy.org- dictionnaire malagasy** – [tenymalagasy.org](https://tenymalagasy.org/bins/homePage) 
- **NLP Libraries** : NLTK, spaCy, RapidFuzz  
- **Scraping** : Requests, BeautifulSoup  
- **TTS** : gTTS  
- Articles et guides sur le NLP Low Resource et la morphologie malagasy


##  Conclusion

Cet éditeur intelligent permet de **faciliter la rédaction en malagasy**, en utilisant des **approches hybrides et explicables**, malgré le manque de données massives.  
L’accent est mis sur la **pertinence linguistique et l’expérience utilisateur** plutôt que sur la taille des modèles.
