# Pour lancer ce script avec docker: docker compose exec web python scripts/creer_dossiers.py

import os
import sys
import django

# --- CONFIGURATION ROBUSTE ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configuration de Django (identique à votre script fonctionnel)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application_web.settings")
django.setup()

from gestion_cycle.models import SiteTouristique

def run():
    # Chemin vers le dossier media
    base_path = os.path.join(project_root, 'gestion_cycle', 'media', 'site_images')

    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"📁 Dossier racine créé : {base_path}")

    sites = SiteTouristique.objects.all()
    print(f"🔍 Traitement de {sites.count()} sites...")

    for site in sites:
        # Nettoyage du nom pour créer un dossier valide (espaces -> _)
        nom_dossier = site.nom.replace(' ', '_').replace("'", "_")
        path = os.path.join(base_path, nom_dossier)
        
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"✅ Dossier créé : {nom_dossier}")
        else:
            print(f"ℹ️  Dossier existant : {nom_dossier}")

if __name__ == "__main__":
    run()