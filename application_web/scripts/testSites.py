import json
import os

# Chemin vers le fichier JSON dans fixtures
json_file = os.path.join('gestion_cycle', 'fixtures', 'sites_touristiques.json')

# Répertoire où sont stockées les images
images_dir = os.path.join('gestion_cycle', 'media', 'sites')

# Champs obligatoires pour chaque site
required_fields = ['nom', 'ville', 'description', 'photo', 'latitude', 'longitude']

# Charger le fichier JSON
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Nombre total d'entrées dans le JSON : {len(data)}\n")

errors = []

for entry in data:
    pk = entry.get('pk', 'N/A')
    fields = entry.get('fields', {})
    missing_fields = [field for field in required_fields if not fields.get(field)]

    # Vérifier les champs obligatoires
    if missing_fields:
        errors.append(f"Entrée PK={pk} : champs manquants -> {missing_fields}")

    # Vérifier si le fichier image existe
    photo_path = fields.get('photo')
    if photo_path:
        full_path = os.path.join(images_dir, os.path.basename(photo_path))
        if not os.path.isfile(full_path):
            errors.append(f"Entrée PK={pk} : image manquante -> {full_path}")
    else:
        errors.append(f"Entrée PK={pk} : aucune photo spécifiée")

# Résultat
if errors:
    print("Problèmes détectés :")
    for e in errors:
        print("-", e)
else:
    print("Toutes les données sont concordantes et toutes les images sont présentes.")
