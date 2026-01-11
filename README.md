# Pandas Psycholinguistique

Projet de conversion de données JSON d'analyses psycholinguistiques en format CSV pour faciliter l'analyse avec pandas.

## Description

Ce projet convertit les données JSON d'expériences psycholinguistiques en fichiers CSV structurés, permettant une analyse plus facile des résultats d'expériences. Il inclut également un module de nettoyage des données pour détecter et supprimer les anomalies.

## Structure du projet

```
.
├── data/                    # Fichiers JSON source
├── export/                  # Fichiers CSV générés (non versionnés)
│   └── clean/              # Fichiers CSV nettoyés et rapports d'anomalies
├── instruction/            # Documentation des commandes
├── convert_to_csv.py       # Script principal de conversion
├── clean_data.py           # Script de nettoyage et détection d'anomalies
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

### 1. Conversion JSON vers CSV

#### Avec npm
```bash
npm run convert
```

#### Avec make
```bash
make convert
```

#### Manuelle
```bash
source venv/bin/activate
python convert_to_csv.py
```

Le script lit le fichier `data/analytics_complete_2026-01-11.json` et génère un fichier CSV dans le dossier `export/` avec le nom `analytics-DD-MM-HH-MM-SS.csv`.

### 2. Nettoyage des données

Le script de nettoyage détecte et supprime les anomalies dans les temps de réponse :
- **Réponses trop rapides** : < 100 ms (0.1 seconde)
- **Réponses trop lentes** : > 600 000 ms (10 minutes)

#### Avec npm
```bash
npm run clean
```

#### Avec make
```bash
make clean
```

#### Manuelle
```bash
source venv/bin/activate
python clean_data.py
```

Le script :
- Analyse automatiquement le fichier CSV le plus récent dans `export/`
- Affiche les statistiques et liste toutes les anomalies détectées
- Génère un fichier CSV nettoyé dans `export/clean/analytics-clean-DD-MM-HH-MM-SS.csv`
- Exporte un fichier JSON dans `export/clean/json/analytics-clean-DD-MM-HH-MM-SS.js`
- Sauvegarde un rapport des anomalies dans `export/clean/anomalies-DD-MM-HH-MM-SS.csv`

## Documentation

Consultez le fichier [instruction/README.md](instruction/README.md) pour plus de détails sur les commandes disponibles.

## Dépendances

- Python 3.x
- pandas >= 2.3.0
