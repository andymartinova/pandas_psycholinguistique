# Instructions d'utilisation

Ce document liste les commandes nécessaires pour convertir le fichier JSON en CSV.

## Commandes

### 1. Créer l'environnement virtuel Python

```bash
python3 -m venv venv
```

**Explication :** Crée un environnement virtuel Python isolé dans le dossier `venv`. Cela permet d'installer les dépendances sans affecter le système Python global.

---

### 2. Activer l'environnement virtuel

```bash
source venv/bin/activate
```

**Explication :** Active l'environnement virtuel créé. Une fois activé, toutes les commandes Python utiliseront cet environnement. Vous verrez `(venv)` dans votre terminal.

---

### 3. Installer les dépendances

```bash
pip install pandas
```

**Explication :** Installe la bibliothèque pandas nécessaire pour la conversion des données JSON en CSV.

---

### 4. Exécuter le script de conversion

```bash
python convert_to_csv.py
```

**Explication :** Lance le script qui lit le fichier JSON `data/analytics_complete_2026-01-11.json` et crée un fichier CSV dans le dossier `export` avec le nom `analytics-DD-MM-HH-MM-SS.csv` (où DD-MM-HH-MM-SS correspond à la date, l'heure, les minutes et les secondes actuelles).

---

### 5. Désactiver l'environnement virtuel (optionnel)

```bash
deactivate
```

**Explication :** Désactive l'environnement virtuel et retourne à l'environnement Python système.

---

## Workflow complet

Pour une première utilisation :

```bash
# 1. Créer l'environnement virtuel
python3 -m venv venv

# 2. L'activer
source venv/bin/activate

# 3. Installer pandas
pip install pandas

# 4. Exécuter le script
python convert_to_csv.py
```

Pour les utilisations suivantes (si l'environnement virtuel existe déjà) :

```bash
# 1. Activer l'environnement virtuel
source venv/bin/activate

# 2. Exécuter le script
python convert_to_csv.py
```

---

## Résultat

Le fichier CSV sera créé dans le dossier `export/` avec un nom au format `analytics-DD-MM-HH-MM-SS.csv` (exemple : `analytics-11-01-14-30-45.csv` pour le 11 janvier à 14h30m45s).
