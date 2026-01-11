import pandas as pd
import os
import json
from datetime import datetime
import glob

# Trouver le fichier CSV le plus récent dans export/
export_dir = "export"
csv_files = glob.glob(os.path.join(export_dir, "analytics-*.csv"))

if not csv_files:
    print("❌ Aucun fichier CSV trouvé dans le dossier export/")
    print("   Exécutez d'abord convert_to_csv.py")
    exit(1)

# Prendre le fichier le plus récent
latest_csv = max(csv_files, key=os.path.getctime)
print(f"📖 Lecture du fichier: {latest_csv}")

# Lire le CSV
df = pd.read_csv(latest_csv)

print(f"\n📊 Statistiques initiales:")
print(f"   Total de lignes: {len(df)}")
print(f"   Nombre de participants: {df['participant_id'].nunique()}")

# Convertir response_time en numérique (au cas où)
df['response_time'] = pd.to_numeric(df['response_time'], errors='coerce')

# Statistiques sur response_time
print(f"\n📈 Statistiques sur response_time:")
mean_rt = df['response_time'].mean()
median_rt = df['response_time'].median()
std_rt = df['response_time'].std()
min_rt = df['response_time'].min()
max_rt = df['response_time'].max()
q1 = df['response_time'].quantile(0.25)
q3 = df['response_time'].quantile(0.75)
iqr = q3 - q1

print(f"   Moyenne: {mean_rt:.2f} ms ({mean_rt/1000:.2f} s)")
print(f"   Médiane: {median_rt:.2f} ms ({median_rt/1000:.2f} s)")
print(f"   Écart-type: {std_rt:.2f} ms ({std_rt/1000:.2f} s)")
print(f"   Minimum: {min_rt:.2f} ms ({min_rt/1000:.2f} s)")
print(f"   Maximum: {max_rt:.2f} ms ({max_rt/60000:.2f} min)")
print(f"   Q1 (25e percentile): {q1:.2f} ms ({q1/1000:.2f} s)")
print(f"   Q3 (75e percentile): {q3:.2f} ms ({q3/1000:.2f} s)")
print(f"   IQR (Interquartile Range): {iqr:.2f} ms ({iqr/1000:.2f} s)")

# Calculer les suggestions de seuils avec différentes méthodes
print(f"\n💡 SUGGESTIONS DE SEUILS (basées sur l'analyse statistique):")
print("=" * 100)

# Méthode 1: IQR (Interquartile Range) - Méthode robuste recommandée
min_iqr = max(0, q1 - 1.5 * iqr)  # Ne pas aller en dessous de 0
max_iqr = q3 + 1.5 * iqr
print(f"\n1️⃣  Méthode IQR (Interquartile Range) - ⭐ RECOMMANDÉE")
print(f"   Seuil minimum suggéré: {min_iqr:.0f} ms ({min_iqr/1000:.2f} s)")
print(f"   Seuil maximum suggéré: {max_iqr:.0f} ms ({max_iqr/60000:.2f} min)")
print(f"   Raison: Méthode robuste qui identifie les valeurs en dehors de 1.5×IQR")

# Méthode 2: Écarts-types (3 sigma)
min_std = max(0, mean_rt - 3 * std_rt)
max_std = mean_rt + 3 * std_rt
print(f"\n2️⃣  Méthode des écarts-types (moyenne ± 3σ)")
print(f"   Seuil minimum suggéré: {min_std:.0f} ms ({min_std/1000:.2f} s)")
print(f"   Seuil maximum suggéré: {max_std:.0f} ms ({max_std/60000:.2f} min)")
print(f"   Raison: Identifie les valeurs à plus de 3 écarts-types de la moyenne")

# Méthode 3: Percentiles
p1 = df['response_time'].quantile(0.01)
p99 = df['response_time'].quantile(0.99)
print(f"\n3️⃣  Méthode des percentiles (1er et 99e percentile)")
print(f"   Seuil minimum suggéré: {p1:.0f} ms ({p1/1000:.2f} s)")
print(f"   Seuil maximum suggéré: {p99:.0f} ms ({p99/60000:.2f} min)")
print(f"   Raison: Conserve 98% des données centrales")

# Méthode 4: Seuils pratiques (basés sur des considérations psycholinguistiques)
min_practical = 200  # 0.1 seconde - temps minimum physiologique
max_practical = 600000  # 10 minutes - temps maximum raisonnable
print(f"\n4️⃣  Méthode pratique (seuils fixes basés sur la littérature)")
print(f"   Seuil minimum suggéré: {min_practical} ms ({min_practical/1000:.1f} s)")
print(f"   Seuil maximum suggéré: {max_practical} ms ({max_practical/60000:.1f} min)")
print(f"   Raison: Seuils standards en psycholinguistique")

# Utiliser la méthode IQR par défaut (la plus robuste)
MIN_RESPONSE_TIME = int(min_iqr)
MAX_RESPONSE_TIME = int(max_iqr)

print(f"\n🔍 SEUILS UTILISÉS (méthode IQR par défaut):")
print(f"   Seuil minimum: {MIN_RESPONSE_TIME} ms ({MIN_RESPONSE_TIME/1000:.2f} s)")
print(f"   Seuil maximum: {MAX_RESPONSE_TIME} ms ({MAX_RESPONSE_TIME/60000:.2f} min)")
print(f"\n   💡 Pour utiliser d'autres seuils, modifiez les variables MIN_RESPONSE_TIME et MAX_RESPONSE_TIME dans le script")

# Détecter les anomalies
anomalies_trop_rapides = df[df['response_time'] < MIN_RESPONSE_TIME]
anomalies_trop_lentes = df[df['response_time'] > MAX_RESPONSE_TIME]
anomalies_total = pd.concat([anomalies_trop_rapides, anomalies_trop_lentes]).drop_duplicates()

print(f"\n⚠️  ANOMALIES DÉTECTÉES:")
print(f"   Réponses trop rapides (< {MIN_RESPONSE_TIME} ms): {len(anomalies_trop_rapides)}")
print(f"   Réponses trop lentes (> {MAX_RESPONSE_TIME} ms): {len(anomalies_trop_lentes)}")
print(f"   Total d'anomalies: {len(anomalies_total)}")

# Afficher les détails des anomalies
if len(anomalies_trop_rapides) > 0:
    print(f"\n🚨 RÉPONSES TROP RAPIDES (< {MIN_RESPONSE_TIME} ms):")
    print("=" * 100)
    for idx, row in anomalies_trop_rapides.iterrows():
        print(f"   Participant: {row['participant_id']} | Trial: {row['trial']} | "
              f"Temps: {row['response_time']:.0f} ms ({row['response_time']/1000:.2f} s) | "
              f"Phrase: {row['sentence'][:50]}...")

if len(anomalies_trop_lentes) > 0:
    print(f"\n🐌 RÉPONSES TROP LENTES (> {MAX_RESPONSE_TIME} ms):")
    print("=" * 100)
    for idx, row in anomalies_trop_lentes.iterrows():
        print(f"   Participant: {row['participant_id']} | Trial: {row['trial']} | "
              f"Temps: {row['response_time']:.0f} ms ({row['response_time']/60000:.2f} min) | "
              f"Phrase: {row['sentence'][:50]}...")

# Statistiques par participant
if len(anomalies_total) > 0:
    print(f"\n👥 ANOMALIES PAR PARTICIPANT:")
    print("=" * 100)
    anomalies_par_participant = anomalies_total.groupby('participant_id').size().sort_values(ascending=False)
    for participant_id, count in anomalies_par_participant.items():
        print(f"   {participant_id}: {count} anomalie(s)")

# Détecter les participants suspects (spam/réponses au hasard)
print(f"\n🔍 DÉTECTION DES PARTICIPANTS SUSPECTS (SPAM/RÉPONSES AU HASARD):")
print("=" * 100)

# Calculer les statistiques par participant
participant_stats = []
for participant_id in df['participant_id'].unique():
    participant_data = df[df['participant_id'] == participant_id]
    total_trials = len(participant_data)
    
    if total_trials == 0:
        continue
    
    # Nombre d'anomalies (séparer trop rapides et trop lentes)
    anomalies_rapides_participant = anomalies_trop_rapides[anomalies_trop_rapides['participant_id'] == participant_id]
    anomalies_lentes_participant = anomalies_trop_lentes[anomalies_trop_lentes['participant_id'] == participant_id]
    anomalies_rapides_count = len(anomalies_rapides_participant)
    anomalies_lentes_count = len(anomalies_lentes_participant)
    anomalies_total_count = anomalies_rapides_count + anomalies_lentes_count
    anomalies_rapides_rate = (anomalies_rapides_count / total_trials) * 100 if total_trials > 0 else 0
    anomalies_total_rate = (anomalies_total_count / total_trials) * 100 if total_trials > 0 else 0
    
    # Taux de réponses correctes
    if 'correct' in participant_data.columns:
        # Gérer différents formats: bool, string "True"/"False", int 1/0
        correct_col = participant_data['correct']
        if correct_col.dtype == bool:
            correct_count = correct_col.sum()
        else:
            # Convertir en booléen pour compter
            correct_count = (
                (correct_col == True) | 
                (correct_col == 'True') | 
                (correct_col == 'true') |
                (correct_col == 1) |
                (correct_col == '1')
            ).sum()
        correct_rate = (correct_count / total_trials) * 100 if total_trials > 0 else 0
    else:
        correct_rate = None
    
    # Temps de réponse moyen
    mean_rt_participant = participant_data['response_time'].mean()
    
    # Critères de suspicion (très restrictifs sur les réponses trop rapides)
    is_suspicious = False
    reasons = []
    
    # Critère 1: Taux de réponses TROP RAPIDES > 15% (très restrictif)
    if anomalies_rapides_rate > 15:
        is_suspicious = True
        reasons.append(f"Taux de réponses trop rapides élevé ({anomalies_rapides_rate:.1f}%)")
    
    # Critère 2: Nombre absolu de réponses trop rapides > 5 (très restrictif)
    if anomalies_rapides_count > 3:
        is_suspicious = True
        reasons.append(f"Nombre de réponses trop rapides élevé ({anomalies_rapides_count})")
    
    # Critère 3: Taux de réponses correctes < 30% (proche du hasard pour binaire)
    if correct_rate is not None and correct_rate < 30:
        is_suspicious = True
        reasons.append(f"Taux de réponses correctes très bas ({correct_rate:.1f}%)")
    
    # Critère 4: Temps de réponse moyen très rapide (< 500ms, très restrictif)
    if pd.notna(mean_rt_participant) and mean_rt_participant < 500:
        is_suspicious = True
        reasons.append(f"Temps de réponse moyen très rapide ({mean_rt_participant:.0f} ms)")
    
    # Note: Les réponses lentes ne sont PAS un critère de suspicion (c'est naturel)
    
    if is_suspicious:
        participant_stats.append({
            'participant_id': participant_id,
            'total_trials': total_trials,
            'anomalies_rapides_count': anomalies_rapides_count,
            'anomalies_lentes_count': anomalies_lentes_count,
            'anomalies_total_count': anomalies_total_count,
            'anomalies_rapides_rate': anomalies_rapides_rate,
            'anomalies_total_rate': anomalies_total_rate,
            'correct_rate': correct_rate,
            'mean_rt': mean_rt_participant,
            'reasons': reasons
        })

# Afficher les participants suspects et demander confirmation
participants_to_exclude = []
if len(participant_stats) > 0:
    print(f"\n⚠️  {len(participant_stats)} participant(s) suspect(s) détecté(s):\n")
    
    for i, stats in enumerate(participant_stats, 1):
        print(f"{'='*100}")
        print(f"🔴 PARTICIPANT SUSPECT #{i}: {stats['participant_id']}")
        print(f"{'='*100}")
        print(f"   📊 Statistiques:")
        print(f"      • Total de trials: {stats['total_trials']}")
        print(f"      • Réponses trop rapides: {stats['anomalies_rapides_count']} ({stats['anomalies_rapides_rate']:.1f}%)")
        print(f"      • Réponses trop lentes: {stats['anomalies_lentes_count']} (non pénalisées)")
        print(f"      • Total d'anomalies: {stats['anomalies_total_count']} ({stats['anomalies_total_rate']:.1f}%)")
        if stats['correct_rate'] is not None:
            print(f"      • Taux de réponses correctes: {stats['correct_rate']:.1f}%")
        if pd.notna(stats['mean_rt']):
            print(f"      • Temps de réponse moyen: {stats['mean_rt']:.0f} ms ({stats['mean_rt']/1000:.2f} s)")
        print(f"   ⚠️  Raisons de suspicion:")
        for reason in stats['reasons']:
            print(f"      • {reason}")
        print()
        
        # Demander confirmation
        while True:
            response = input(f"   ❓ Exclure ce participant des statistiques ? (y/n): ").strip().lower()
            if response in ['y', 'yes', 'o', 'oui']:
                participants_to_exclude.append(stats['participant_id'])
                print(f"   ✓ Participant {stats['participant_id']} sera exclu\n")
                break
            elif response in ['n', 'no', 'non']:
                print(f"   → Participant {stats['participant_id']} sera conservé\n")
                break
            else:
                print("   ❌ Réponse invalide. Veuillez répondre 'y' ou 'n'")
else:
    print("   ✓ Aucun participant suspect détecté")

# Créer le DataFrame nettoyé (sans les anomalies ET sans les participants exclus)
df_clean = df[
    (df['response_time'] >= MIN_RESPONSE_TIME) & 
    (df['response_time'] <= MAX_RESPONSE_TIME) &
    (~df['participant_id'].isin(participants_to_exclude))
].copy()

print(f"\n✨ NETTOYAGE:")
print(f"   Lignes avant nettoyage: {len(df)}")
excluded_rows = 0
if len(participants_to_exclude) > 0:
    excluded_rows = len(df[df['participant_id'].isin(participants_to_exclude)])
    print(f"   Participants exclus: {len(participants_to_exclude)} ({excluded_rows} lignes)")
    print(f"      → {', '.join(participants_to_exclude)}")
print(f"   Lignes supprimées (anomalies): {len(df) - len(df_clean) - excluded_rows}")
print(f"   Lignes après nettoyage: {len(df_clean)}")
print(f"   Pourcentage conservé: {len(df_clean)/len(df)*100:.2f}%")
print(f"   Nombre de participants restants: {df_clean['participant_id'].nunique()}")

# Créer le dossier export/clean/ s'il n'existe pas
clean_dir = os.path.join(export_dir, "clean")
os.makedirs(clean_dir, exist_ok=True)

# Générer le nom de fichier avec la date et l'heure actuelle (DD-MM-HH-MM-SS)
now = datetime.now()
filename = f"analytics-clean-{now.strftime('%d-%m-%H-%M-%S')}.csv"
filepath = os.path.join(clean_dir, filename)

# Sauvegarder le CSV nettoyé
print(f"\n💾 Sauvegarde du fichier nettoyé dans {filepath}...")
df_clean.to_csv(filepath, index=False, encoding='utf-8')

print(f"✓ Nettoyage terminé ! {len(df_clean)} lignes exportées dans {filepath}")

# Créer le dossier export/clean/json/ s'il n'existe pas
json_dir = os.path.join(clean_dir, "json")
os.makedirs(json_dir, exist_ok=True)

# Exporter en JSON avec le même format que le fichier d'entrée
json_filename = f"analytics-clean-{now.strftime('%d-%m-%H-%M-%S')}.json"
json_filepath = os.path.join(json_dir, json_filename)
print(f"\n💾 Export JSON dans {json_filepath}...")

# Trouver le fichier JSON le plus récent dans data/
data_dir = "data"
json_files = glob.glob(os.path.join(data_dir, "*.json"))

if not json_files:
    print("❌ Aucun fichier JSON trouvé dans le dossier data/")
    exit(1)

# Prendre le fichier le plus récent
original_json_file = max(json_files, key=os.path.getctime)
print(f"📖 Lecture du fichier JSON original: {original_json_file}")

# Lire le JSON original pour récupérer la structure et les métadonnées
with open(original_json_file, 'r', encoding='utf-8') as f:
    original_data = json.load(f)

# Reconstruire la structure JSON originale avec les données nettoyées
imported_data_clean = []

# Grouper les données nettoyées par participant
for participant_id in df_clean['participant_id'].unique():
    participant_data_clean = df_clean[df_clean['participant_id'] == participant_id]
    
    # Trouver les métadonnées du participant dans le JSON original
    participant_metadata = None
    for item in original_data.get("importedData", []):
        if item.get("data", {}).get("participant", {}).get("id") == participant_id:
            participant_metadata = item
            break
    
    if participant_metadata is None:
        continue
    
    # Reconstruire les données du participant
    participant_info = participant_data_clean.iloc[0]
    
    # Trier les trials par numéro de trial
    participant_data_sorted = participant_data_clean.sort_values('trial')
    
    # Reconstruire les trials
    experiment_data = []
    for _, row in participant_data_sorted.iterrows():
        # Gérer les valeurs booléennes correctement
        correct_value = row['correct']
        if pd.notna(correct_value):
            if isinstance(correct_value, bool):
                correct_value = correct_value
            elif isinstance(correct_value, str):
                correct_value = correct_value.lower() in ['true', '1']
            elif isinstance(correct_value, (int, float)):
                correct_value = bool(correct_value)
        else:
            correct_value = None
        
        trial_data = {
            "trial": int(row['trial']) if pd.notna(row['trial']) else None,
            "sentence": row['sentence'] if pd.notna(row['sentence']) else None,
            "condition": row['condition'] if pd.notna(row['condition']) else None,
            "expected": row['expected'] if pd.notna(row['expected']) else None,
            "response": row['response'] if pd.notna(row['response']) else None,
            "responseTime": int(row['response_time']) if pd.notna(row['response_time']) else None,
            "correct": correct_value
        }
        experiment_data.append(trial_data)
    
    # Reconstruire la structure complète
    participant_entry = {
        "name": participant_metadata.get("name", f"Participant {participant_id} - Database"),
        "size": participant_metadata.get("size", 0),
        "lastModified": participant_metadata.get("lastModified", int(datetime.now().timestamp() * 1000)),
        "data": {
            "participant": {
                "id": participant_id,
                "languageGroup": participant_info['language_group'] if pd.notna(participant_info['language_group']) else None,
                "germanLevel": participant_info['german_level'] if pd.notna(participant_info['german_level']) else None,
                "learningDuration": participant_info['learning_duration'] if pd.notna(participant_info['learning_duration']) else None,
                "startTime": participant_info['start_time'] if pd.notna(participant_info['start_time']) else None
            },
            "experiment": {
                "config": participant_metadata.get("data", {}).get("experiment", {}).get("config", {}),
                "endTime": participant_info['end_time'] if pd.notna(participant_info['end_time']) else None,
                "data": experiment_data
            }
        }
    }
    
    imported_data_clean.append(participant_entry)

# Créer la structure JSON finale
json_output = {
    "importedData": imported_data_clean
}

# Sauvegarder le JSON
with open(json_filepath, 'w', encoding='utf-8') as f:
    json.dump(json_output, f, ensure_ascii=False, indent=2)

print(f"✓ Export JSON terminé ! {len(imported_data_clean)} participant(s) exporté(s) dans {json_filepath}")

# Sauvegarder aussi un rapport des anomalies
if len(anomalies_total) > 0:
    anomalies_filepath = os.path.join(clean_dir, f"anomalies-{now.strftime('%d-%m-%H-%M-%S')}.csv")
    anomalies_total.to_csv(anomalies_filepath, index=False, encoding='utf-8')
    print(f"✓ Rapport des anomalies sauvegardé dans {anomalies_filepath}")
