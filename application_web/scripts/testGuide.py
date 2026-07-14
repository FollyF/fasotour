import json
import os
import sys
import django

# Ajouter le dossier parent de "application_web" au PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Monter d'un niveau depuis script/
sys.path.append(BASE_DIR)

# Définir le module settings correct
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application_web.settings")

# Initialiser Django
django.setup()

from gestion_cycle.models import Guide

# Chemin vers le fichier JSON dans fixtures
JSON_FILE = os.path.join(BASE_DIR, 'gestion_cycle', 'fixtures', 'guides.json')

# Répertoire où sont stockées les images
IMAGES_DIR = os.path.join(BASE_DIR, 'gestion_cycle', 'media', 'guides')

def run():
    created_count = 0
    updated_count = 0

    print("📌 Importation des guides depuis guides.json...")

    # Charger le fichier JSON avec gestion des erreurs
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Erreur : Le fichier {JSON_FILE} est introuvable.")
        return
    except json.JSONDecodeError:
        print(f"⚠️ Erreur : Le fichier {JSON_FILE} n'est pas un JSON valide.")
        return

    print(f"Nombre total d'entrées dans le JSON : {len(data)}\n")

    errors = []

    for entry in data:
        pk = entry.get('pk', 'N/A')
        fields = entry.get('fields', {})

        # Vérifier les champs obligatoires
        required_fields = ['nom', 'prenom']
        missing_fields = [field for field in required_fields if not fields.get(field)]
        if missing_fields:
            errors.append(f"Entrée PK={pk} : champs obligatoires manquants -> {missing_fields}")
            continue

        # Préparer les données pour update_or_create
        guide_data = {
            'nom': fields['nom'],
            'prenom': fields['prenom'],
            'telephone': fields.get('telephone'),
            'email': fields.get('email'),
            'description': fields.get('description'),
        }

        # Gérer la photo
        photo_path = fields.get('photo')
        if photo_path:
            normalized_path = os.path.normpath(photo_path)
            full_path = os.path.join(IMAGES_DIR, os.path.basename(normalized_path))
            if os.path.isfile(full_path):
                guide_data['photo'] = full_path  # À ajuster pour un FileField si nécessaire
            else:
                errors.append(f"Entrée PK={pk} : image manquante -> {full_path}")
                continue
        elif 'photo' in fields and fields['photo'] is None:
            guide_data['photo'] = None  # Accepter None si nullable
        else:
            errors.append(f"Entrée PK={pk} : aucune photo spécifiée (champ nullable attendu)")
            continue

        # Utiliser update_or_create pour insérer ou mettre à jour
        guide, created = Guide.objects.update_or_create(
            pk=pk,
            defaults=guide_data
        )

        if created:
            created_count += 1
            print(f"✅ Guide créé : {guide}")
        else:
            updated_count += 1
            print(f"🔄 Guide mis à jour : {guide}")

    # Afficher les erreurs s'il y en a
    if errors:
        print("\n⚠️ Problèmes détectés :")
        for e in errors:
            print(f"- {e}")
    else:
        print("\n📊 Toutes les données sont concordantes et toutes les images sont présentes.")

    print(f"\n📊 Import terminé ! {created_count} guides créés, {updated_count} guides mis à jour.")

if __name__ == "__main__":
    run()