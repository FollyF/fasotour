import csv
import os
import sys
import django

# Ajouter le dossier parent de "application_web" au PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Définir le module settings correct
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application_web.settings")

# Initialiser Django
django.setup()

from gestion_cycle.models import Ville

CSV_FILE = os.path.join(os.path.dirname(__file__), "bf.csv")

def run():
    created_count = 0
    updated_count = 0

    print("📌 Importation des villes depuis bf.csv...")

    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertir latitude et longitude en float si possible
            try:
                lat = float(row["lat"]) if row["lat"] else None
                lng = float(row["lng"]) if row["lng"] else None
            except ValueError:
                print(f"⚠️ Coordonnées invalides pour la ville {row['city']}, ligne ignorée.")
                continue

            if lat is None or lng is None:
                print(f"⚠️ Latitude ou longitude manquante pour la ville {row['city']}, ligne ignorée.")
                continue

            ville, created = Ville.objects.update_or_create(
                latitude=lat,
                longitude=lng,
                defaults={
                    "nom": row["city"],
                    "pays": row.get("country", "Burkina Faso"),
                    "code_iso2": row.get("iso2", "BF"),
                    "region": row.get("admin_name") or None,
                    "statut": row.get("capital") or None,
                    "population": int(row["population"]) if row["population"] else None,
                    "population_propre": int(row["population_proper"]) if row["population_proper"] else None,
                }
            )

            if created:
                created_count += 1
                print(f"✅ Ville créée : {row['city']}")
            else:
                updated_count += 1
                print(f"🔄 Ville mise à jour : {row['city']}")

    print(f"\n📊 Import terminé ! {created_count} villes créées, {updated_count} villes mises à jour.")

if __name__ == "__main__":
    run()
