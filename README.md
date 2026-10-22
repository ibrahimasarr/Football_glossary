# ⚽ Pulaar Football Glossary & Localization

Ce projet est une initiative linguistique visant à documenter, enrichir et standardiser le lexique du football (soccer) en **Pulaar (Fulfulde)**. L'objectif principal est de permettre de commenter, d'analyser et de débattre du football de manière fluide en utilisant exclusivement les ressources morphologiques du Pulaar, sans recourir aux emprunts systémiques de l'anglais ou du français.

## 🎯 Objectifs du Projet

- **Anti-Emprunt Strict** : Remplacer le vocabulaire technique occidental par des néologismes, des dérivés verbaux ou des concepts traditionnels pulaar adaptés.
- **Approche Structurée** : Utilisation du format de localisation standardisé **Gettext (.po)** pour faciliter l'intégration future du lexique dans des applications web, mobiles ou des plateformes de sous-titrage vidéo.
- **Validation Automatisée** : Intégration d'un pipeline d'intégration continue (CI) pour traquer les biais de traduction et classifier les termes par classes nominales.

## 📂 Structure du Dépôt

```text
├── .github/workflows/   # Pipeline d'automatisation GitHub Actions
├── locales/
│   └── ff/
│       └── football.po  # Le fichier maître contenant le glossaire traduit
├── valider_lexique.py   # Script Python de contrôle de conformité linguistique
└── README.md            # Présentation du projet
```

## 🛠️ Validation Automatique & Qualité Linguistique

Le projet intègre un script Python (`valider_lexique.py`) exécuté automatiquement à chaque modification (`git push`). Ce script garantit deux garde-fous :

1. **Zéro pollution linguistique** : Il compare la chaîne Pulaar avec les chaînes sources anglaises et françaises pour rejeter toute intégration accidentelle de mots occidentaux non traduits.
2. **Cohérence morphosyntaxique** : Il classe dynamiquement les termes créés selon leurs suffixes pour assurer un équilibre harmonieux entre les classes nominales pulaar (_ngal, ka, ɗam, o, ɗi_, etc.).

## 🚀 Comment contribuer ou tester localement

Si vous êtes un spécialiste de la langue Pulaar ou un développeur intéressé par la localisation :

1. Clonez le dépôt :
   ```bash
   git clone https://github.com
   ```
2. Installez la dépendance de contrôle :
   ```bash
   pip install polib
   ```
3. Ouvrez le fichier `locales/ff/football.po` avec **VS Code** (en installant l'extension _PO File Support_) ou via le logiciel **Poedit** pour enrichir la base de données.
4. Lancez le script de validation :
   ```bash
   python valider_lexique.py
   ```

## 📄 Licence

Ce projet est sous licence MIT. N'hésitez pas à l'utiliser, le modifier et le partager pour faire rayonner la langue Pulaar dans l'écosystème numérique sportif.
