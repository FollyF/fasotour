import csv
import os
import sys
import django

# --- CONFIGURATION ROBUSTE ---
# On récupère le répertoire du script actuel
script_dir = os.path.dirname(os.path.abspath(__file__))

# La racine du projet est le dossier parent du dossier 'scripts'
project_root = os.path.dirname(script_dir)

# On ajoute la racine au PYTHONPATH si ce n'est pas déjà fait
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configuration de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application_web.settings")
django.setup()

# Importation du modèle après django.setup()
from gestion_cycle.models import Ville

CSV_FILE = os.path.join(script_dir, "bf.csv")

def run():
    if not os.path.exists(CSV_FILE):
        print(f"❌ Erreur : Le fichier {CSV_FILE} est introuvable.")
        return

    created_count = 0
    updated_count = 0

    print(f"📌 Importation des villes depuis {CSV_FILE}...")

    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Gestion sécurisée des nombres
                lat_str = row.get("lat")
                lng_str = row.get("lng")
                
                lat = float(lat_str) if lat_str else None
                lng = float(lng_str) if lng_str else None
            except ValueError:
                print(f"⚠️ Coordonnées invalides pour {row.get('city', 'Inconnue')}, ligne ignorée.")
                continue

            if lat is None or lng is None:
                continue

            # Utilisation de update_or_create
            ville, created = Ville.objects.update_or_create(
                latitude=lat,
                longitude=lng,
                defaults={
                    "nom": row.get("city"),
                    "pays": row.get("country", "Burkina Faso"),
                    "code_iso2": row.get("iso2", "BF"),
                    "region": row.get("admin_name") or None,
                    "statut": row.get("capital") or None,
                    "population": int(row["population"]) if row.get("population") else None,
                    "population_propre": int(row["population_proper"]) if row.get("population_proper") else None,
                }
            )

            if created:
                created_count += 1
                print(f"✅ Ville créée : {row.get('city')}")
            else:
                updated_count += 1
                print(f"🔄 Ville mise à jour : {row.get('city')}")

    print(f"\n📊 Import terminé ! {created_count} créées, {updated_count} mises à jour.")

if __name__ == "__main__":
    run()