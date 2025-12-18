# ChatBox

Application de messagerie instantanée développée avec [Angular](https://angular.io/) et [Angular CLI](https://github.com/angular/angular-cli) version 20.3.8.

## 📋 Prérequis

- Node.js (version 18 ou supérieure)
- npm (version 9 ou supérieure) ou yarn
- Angular CLI (installé globalement avec `npm install -g @angular/cli`)

## 🚀 Installation

1. Cloner le dépôt :
   ```bash
   git clone [URL_DU_DEPOT]
   cd chatBox
   ```

2. Installer les dépendances :
   ```bash
   npm install
   # ou
   yarn install
   ```

## 🛠 Développement

Pour démarrer le serveur de développement :

```bash
ng serve
```

Ouvrez votre navigateur à l'adresse `http://localhost:4200/`. L'application se rechargera automatiquement à chaque modification des fichiers sources.

### Commandes utiles

- **Générer un composant** :
  ```bash
  ng generate component nom-du-composant
  ```

- **Construire le projet** (production) :
  ```bash
  ng build --configuration production
  ```
  Les fichiers compilés seront disponibles dans le dossier `dist/`.

## 🧪 Tests

### Tests unitaires

```bash
ng test
```

### Tests e2e (End-to-End)

```bash
ng e2e
```

## 📦 Déploiement

Pour déployer sur un serveur, utilisez :

```bash
ng build --configuration production
```

Les fichiers de production seront générés dans le dossier `dist/chat-box/`.

## 📂 Structure du projet

```
src/
├── app/                 # Code source de l'application
│   ├── components/      # Composants réutilisables
│   ├── services/        # Services Angular
│   └── ...
├── assets/             # Fichiers statiques (images, polices, etc.)
└── environments/       # Configurations d'environnement
```

## 🤝 Contribution

1. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-nouvelle-fonctionnalite`)
2. Committez vos changements (`git commit -am 'Ajout d\'une nouvelle fonctionnalité'`)
3. Poussez vers la branche (`git push origin feature/ma-nouvelle-fonctionnalite`)
4. Créez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
