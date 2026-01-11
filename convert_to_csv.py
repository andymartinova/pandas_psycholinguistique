import json
import pandas as pd
import os
from datetime import datetime

# Chemin du fichier JSON source
json_file = "data/analytics_complete_2026-01-11.json"

# Lire le fichier JSON
print(f"Lecture du fichier {json_file}...")
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extraire les données et les aplatir
rows = []
for item in data.get("importedData", []):
    participant = item.get("data", {}).get("participant", {})
    experiment = item.get("data", {}).get("experiment", {})
    
    participant_id = participant.get("id")
    language_group = participant.get("languageGroup")
    german_level = participant.get("germanLevel")
    learning_duration = participant.get("learningDuration")
    start_time = participant.get("startTime")
    end_time = experiment.get("endTime")
    
    # Pour chaque trial dans l'expérience
    for trial in experiment.get("data", []):
        row = {
            "participant_id": participant_id,
            "language_group": language_group,
            "german_level": german_level,
            "learning_duration": learning_duration,
            "start_time": start_time,
            "end_time": end_time,
            "trial": trial.get("trial"),
            "sentence": trial.get("sentence"),
            "condition": trial.get("condition"),
            "expected": trial.get("expected"),
            "response": trial.get("response"),
            "response_time": trial.get("responseTime"),
            "correct": trial.get("correct")
        }
        rows.append(row)

# Créer un DataFrame pandas
df = pd.DataFrame(rows)

# Créer le dossier export s'il n'existe pas
export_dir = "export"
os.makedirs(export_dir, exist_ok=True)

# Générer le nom de fichier avec la date et l'heure actuelle (DD-MM-HH-MM)
now = datetime.now()
filename = f"analytics-{now.strftime('%d-%m-%H-%M')}.csv"
filepath = os.path.join(export_dir, filename)

# Sauvegarder en CSV
print(f"Sauvegarde dans {filepath}...")
df.to_csv(filepath, index=False, encoding='utf-8')

print(f"✓ Conversion terminée ! {len(df)} lignes exportées dans {filepath}")
