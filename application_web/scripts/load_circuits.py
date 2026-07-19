import os
import sys
import django

# --- 1. CONFIGURATION ROBUSTE DU CHEMIN ---
# On détecte automatiquement la racine du projet où se trouve manage.py
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_script_dir)

# On ajoute la racine au PYTHONPATH pour que 'gestion_cycle' soit visible
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configuration de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application_web.settings")
django.setup()

# --- 2. IMPORT DU MODÈLE ---
from gestion_cycle.models import Circuit

def run():
    # Liste des circuits à insérer
    circuits_data = [
        ("Circuit des Joyaux du Sahel", "Une aventure inoubliable à travers le désert, à la découverte des trésors cachés et des traditions nomades du nord du pays.", 7),
        ("Sur la Route des Savanes", "Un voyage immersif au cœur des savanes, à la rencontre de la faune sauvage et des villages traditionnels de l'ouest burkinabè.", 5),
        ("L'Épopée du Royaume Mossi", "Explorez l'histoire et la culture de l'ancien empire Mossi, de la capitale Ouagadougou aux villages des alentours.", 3),
        ("Circuit des Cascadelles", "Une escapade rafraîchissante pour découvrir les cascades et les paysages luxuriants du sud-ouest, idéal pour les amateurs de nature.", 4),
        ("Aventure Gourmande à Bobo", "Plongez dans l'ambiance unique de Bobo-Dioulasso et savourez la gastronomie locale tout en explorant ses sites emblématiques.", 2),
        ("Circuit du Pays Lobi", "Découvrez l'architecture fortifiée et les coutumes fascinantes du peuple Lobi dans le sud-ouest du Burkina.", 3),
        ("Escapade au Pays Dogon", "Une incursion culturelle et spirituelle pour explorer les falaises, les grottes et les traditions ancestrales du peuple Dogon.", 6),
        ("Les Trésors du Gourma", "Un circuit pour les passionnés d'histoire, d'art et de culture, à travers les sites historiques et les marchés de la région du Gourma.", 5),
        ("Le Sentier des Artisans", "Une immersion dans l'artisanat burkinabè, de la poterie à la sculpture, en visitant les ateliers et les villages d'artistes.", 4),
        ("Randonnée dans le Parc National d'Arly", "Un circuit pour les amoureux de la nature, avec des safaris, des randonnées et des observations d'animaux dans l'un des plus beaux parcs du pays.", 2)
    ]

    print("📌 Début de l'insertion des circuits...")
    
    count = 0
    for nom, desc, jours in circuits_data:
        # Utilisation de get_or_create pour éviter les doublons
        circuit, created = Circuit.objects.get_or_create(
            nom=nom,
            defaults={
                "description": desc,
                "nb_jours": jours
            }
        )
        if created:
            print(f"✅ Circuit créé : {nom}")
            count += 1
        else:
            print(f"ℹ️  Circuit déjà existant : {nom}")

    print(f"\n📊 Import terminé ! {count} nouveaux circuits insérés.")

if __name__ == "__main__":
    run()