import os
import sys
import django

# --- 1. Détection robuste de la racine du projet ---
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = current_dir
found = False

# Remonte les dossiers jusqu'à trouver manage.py
while True:
    if os.path.exists(os.path.join(base_dir, "manage.py")):
        found = True
        break
    parent_dir = os.path.dirname(base_dir)
    if parent_dir == base_dir:  # Arrivé à la racine du système
        break
    base_dir = parent_dir

if not found:
    raise FileNotFoundError("❌ Impossible de localiser 'manage.py'. Ce script doit être dans le projet.")

# Ajout prioritaire au PYTHONPATH
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# --- 2. Configuration Django ---
# 'application_web.settings' est le chemin classique, ajustez si votre projet a un autre nom
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application_web.settings')
django.setup()

# --- 3. Import des modèles ---
from gestion_cycle.models import CategorieSite

def main():
    # Liste des catégories
    categories = [
        "Musée", "Monument historique", "Parc naturel", "Site archéologique",
        "Église / Mosquée / Temple", "Plage", "Forêt / Parc national",
        "Lac / Rivière", "Village culturel", "Centre artisanal",
        "Château / Palais", "Autre"
    ]

    print(f"🚀 Initialisation des catégories dans la base de données...")

    count_created = 0
    for nom in categories:
        cat, created = CategorieSite.objects.get_or_create(
            nom=nom,
            defaults={"description": f"Catégorie dédiée aux sites de type : {nom}"}
        )
        if created:
            print(f"✅ Catégorie '{nom}' créée.")
            count_created += 1
        else:
            print(f"ℹ️  Catégorie '{nom}' existe déjà.")

    print(f"\n✨ Terminé ! {count_created} nouvelles catégories ajoutées.")

if __name__ == "__main__":
    main()