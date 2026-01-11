import pandas as pd
import os
from datetime import datetime

# Chemin du fichier CSV clean
input_file = "export/clean/analytics-clean-11-01-17-01-36.csv"

print(f"📖 Lecture du fichier: {input_file}")

# Lire le CSV
df = pd.read_csv(input_file)

print(f"   Total de lignes: {len(df)}")

# Vérifier que la colonne 'condition' existe
if 'condition' not in df.columns:
    print("❌ Erreur: La colonne 'condition' n'existe pas dans le fichier CSV")
    exit(1)

# Afficher les valeurs uniques de condition pour vérification
print(f"\n📊 Valeurs uniques dans 'condition':")
print(df['condition'].value_counts())

# Créer les deux nouvelles colonnes en séparant 'condition'
def extract_complexite(condition):
    """Extrait la complexité (simple ou complex)"""
    if pd.isna(condition):
        return None
    if 'simple' in condition.lower():
        return 'simple'
    elif 'complex' in condition.lower():
        return 'complex'
    return None

def extract_ambiguite(condition):
    """Extrait l'ambiguité (ambiguous ou non_ambiguous)"""
    if pd.isna(condition):
        return None
    if 'ambiguous' in condition.lower():
        if 'non_ambiguous' in condition.lower():
            return 'non_ambiguous'
        else:
            return 'ambiguous'
    return None

# Ajouter les nouvelles colonnes
df['Complexité'] = df['condition'].apply(extract_complexite)
df['Ambiguité'] = df['condition'].apply(extract_ambiguite)

# Vérifier les valeurs
print(f"\n✅ Colonnes ajoutées:")
print(f"   Complexité - valeurs: {df['Complexité'].value_counts().to_dict()}")
print(f"   Ambiguité - valeurs: {df['Ambiguité'].value_counts().to_dict()}")

# Créer le dossier export/clean/ s'il n'existe pas
clean_dir = "export/clean"
os.makedirs(clean_dir, exist_ok=True)

# Générer le nom de fichier avec la date et l'heure actuelle
now = datetime.now()
filename = f"analytics-clean-anova-{now.strftime('%d-%m-%H-%M-%S')}.csv"
filepath = os.path.join(clean_dir, filename)

# Sauvegarder le nouveau CSV
print(f"\n💾 Sauvegarde du fichier avec colonnes ANOVA dans {filepath}...")
df.to_csv(filepath, index=False, encoding='utf-8')

print(f"✓ Fichier créé avec succès ! {len(df)} lignes exportées dans {filepath}")
print(f"\n📋 Colonnes dans le nouveau fichier:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i}. {col}")
