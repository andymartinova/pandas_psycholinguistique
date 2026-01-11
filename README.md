# Pandas Psycholinguistique

Projet de conversion de données JSON d'analyses psycholinguistiques en format CSV pour faciliter l'analyse avec pandas.

## Description

Ce projet convertit les données JSON d'expériences psycholinguistiques en fichiers CSV structurés, permettant une analyse plus facile des résultats d'expériences.

## Structure du projet

```
.
├── data/                    # Fichiers JSON source
├── export/                  # Fichiers CSV générés (non versionnés)
├── instruction/            # Documentation des commandes
├── convert_to_csv.py       # Script principal de conversion
├── requirements.txt        # Dépendances Python
├── package.json           # Scripts npm pour faciliter l'exécution
└── Makefile               # Commandes make alternatives
```

## Installation

### Méthode 1 : Avec npm (recommandé)

```bash
npm run setup
```

### Méthode 2 : Avec make

```bash
make setup
```

### Méthode 3 : Manuelle

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

### Avec npm

```bash
npm run convert
```

### Avec make

```bash
make convert
```

### Manuelle

```bash
source venv/bin/activate
python convert_to_csv.py
```

Le script lit le fichier `data/analytics_complete_2026-01-11.json` et génère un fichier CSV dans le dossier `export/` avec le nom `analytics-DD-MM-HH-MM.csv`.

## Documentation

Consultez le fichier [instruction/README.md](instruction/README.md) pour plus de détails sur les commandes disponibles.

## Dépendances

- Python 3.x
- pandas >= 2.3.0
