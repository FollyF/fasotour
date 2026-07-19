import json
import os
import sys
import django
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError

# --- 1. Détection robuste de la racine du projet ---
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = current_dir
while not os.path.exists(os.path.join(base_dir, "manage.py")):
    parent = os.path.dirname(base_dir)
    if parent == base_dir: # Racine du système atteinte
        raise FileNotFoundError("❌ Impossible de localiser 'manage.py'.")
    base_dir = parent

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# --- 2. Configuration Django ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application_web.settings")
django.setup()

from gestion_cycle.models import Guide

# --- 3. Chemins dynamiques ---
JSON_FILE = os.path.join(base_dir, 'gestion_cycle', 'fixtures', 'guides.json')
IMAGES_DIR = os.path.join(base_dir, 'gestion_cycle', 'media', 'guides')

def run():
    created_count = 0
    updated_count = 0
    errors = []

    print("📌 Début de l'importation des guides...")

    if not os.path.exists(JSON_FILE):
        print(f"⚠️ Erreur : Le fichier {JSON_FILE} est introuvable.")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Erreur : Format JSON invalide.")
            return

    for entry in data:
        pk = entry.get('pk')
        fields = entry.get('fields', {})

        # Vérification champs requis
        if not fields.get('nom') or not fields.get('prenom'):
            errors.append(f"PK={pk} : nom/prénom manquants.")
            continue

        guide_data = {
            'nom': fields['nom'],
            'prenom': fields['prenom'],
            'telephone': fields.get('telephone'),
            'email': fields.get('email'),
            'description': fields.get('description'),
        }

        # Gestion image
        photo_name = fields.get('photo')
        if photo_name:
            full_path = os.path.join(IMAGES_DIR, os.path.basename(photo_name))
            if os.path.isfile(full_path):
                try:
                    with open(full_path, 'rb') as img_file:
                        relative_path = f'guides/{os.path.basename(photo_name)}'
                        # On sauvegarde sans écraser si déjà présent, ou on force selon besoin
                        final_path = default_storage.save(relative_path, img_file)
                        guide_data['photo'] = final_path
                except Exception as e:
                    errors.append(f"PK={pk} : erreur image -> {e}")
                    continue
            else:
                errors.append(f"PK={pk} : image {photo_name} non trouvée sur le disque.")
                continue

        # Sauvegarde
        try:
            guide, created = Guide.objects.update_or_create(pk=pk, defaults=guide_data)
            if created:
                created_count += 1
            else:
                updated_count += 1
        except Exception as e:
            errors.append(f"PK={pk} : erreur DB -> {e}")

    # Rapport final
    if errors:
        print("\n⚠️ Erreurs rencontrées :")
        for e in errors: print(f"- {e}")
    
    print(f"\n📊 Import terminé : {created_count} créés, {updated_count} mis à jour.")

if __name__ == "__main__":
    run()