import os
import sys
import django

# --- Détecter automatiquement la racine du projet (où se trouve manage.py) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = current_dir
found = False

while base_dir != os.path.dirname(base_dir):  # tant qu'on n'est pas à la racine du disque
    if os.path.exists(os.path.join(base_dir, "manage.py")):
        found = True
        break
    base_dir = os.path.dirname(base_dir)

if not found:
    raise FileNotFoundError("Impossible de trouver manage.py. Placez ce scripts dans un sous-dossier du projet.")

# Ajouter la racine du projet au PATH
if base_dir not in sys.path:
    sys.path.append(base_dir)

# --- Configurer Django ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application_web.settings')
django.setup()

# --- Import des modèles ---
from gestion_cycle.models import CategorieSite

# --- Liste des catégories à créer ---
categories = [
    "Musée",
    "Monument historique",
    "Parc naturel",
    "Site archéologique",
    "Église / Mosquée / Temple",
    "Plage",
    "Forêt / Parc national",
    "Lac / Rivière",
    "Village culturel",
    "Centre artisanal",
    "Château / Palais",
    "Autre"
]

# --- Création automatique ---
for nom in categories:
    cat, created = CategorieSite.objects.get_or_create(
        nom=nom,
        defaults={"description": f"Categorie : {nom}"}
    )
    if created:
        print(f"✅ Catégorie '{nom}' créée")
    else:
        print(f"ℹ️ Catégorie '{nom}' existe déjà")

print("✅ Toutes les catégories de sites touristiques ont été créées !")
