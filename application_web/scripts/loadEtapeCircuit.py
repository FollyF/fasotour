import os
import sys
import django

# --- 1. DÉTECTION ROBUSTE DE LA RACINE ---
# Ce bloc garantit que Python trouvera toujours votre projet, où que soit le script
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configuration de l'environnement Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application_web.settings")
django.setup()

# --- 2. IMPORTATIONS APRÈS CONFIGURATION ---
from gestion_cycle.models import Circuit, SiteTouristique, CircuitEtape

def run():
    # Données des circuits
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

    # Données des étapes
    circuits_etapes = {
        "Circuit des Joyaux du Sahel": ["Musée National du Burkina Faso", "Village Artisanal de Ouagadougou (VAO)", "Site de sculptures de Laongo", "Vieilles Mosquées de Bani", "Réserve Naturelle Intégrale de Nazinga", "Cour Royale de Tiébélé", "Ruines de Loropéni"],
        "Sur la Route des Savanes": ["Grande Mosquée de Dioulassoba", "Dômes de Fabédougou", "Cascades de Karfiguéla", "Lac de Tengréla", "Mare aux hippopotames"],
        "L'Épopée du Royaume Mossi": ["Musée National du Burkina Faso", "Place de la Révolution", "Village Artisanal de Ouagadougou (VAO)", "Site de sculptures de Laongo", "Salon international de l'artisanat de Ouagadougou (SIAO)", "Festival panafricain du cinéma et de la télévision de Ouagadougou (FESPACO)"],
        "Circuit des Cascadelles": ["Dômes de Fabédougou", "Lac de Tengréla", "Cascades de Karfiguéla", "Pics de Sindou", "Caverne de Douna"],
        "Aventure Gourmande à Bobo": ["Grande Mosquée de Dioulassoba", "Mare aux hippopotames", "Dômes de Fabédougou", "Lac de Tengréla", "Cascades de Karfiguéla", "Pics de Sindou"],
        "Circuit du Pays Lobi": ["Cour Royale de Tiébélé", "Réserve Naturelle Intégrale de Nazinga", "Ruines de Loropéni", "Pics de Sindou", "Caverne de Douna"],
        "Escapade au Pays Dogon": ["Vieilles Mosquées de Bani", "Cour Royale de Tiébélé", "Ruines de Loropéni", "Pics de Sindou", "Caverne de Douna", "Grande Mosquée de Dioulassoba"],
        "Les Trésors du Gourma": ["Musée National du Burkina Faso", "Village Artisanal de Ouagadougou (VAO)", "Réserve Naturelle Intégrale de Nazinga", "Cour Royale de Tiébélé", "Ruines de Loropéni", "Vieilles Mosquées de Bani"],
        "Le Sentier des Artisans": ["Village Artisanal de Ouagadougou (VAO)", "Salon international de l'artisanat de Ouagadougou (SIAO)", "Musée National du Burkina Faso", "Site de sculptures de Laongo", "Grande Mosquée de Dioulassoba"],
        "Randonnée dans le Parc National d'Arly": ["Réserve Naturelle Intégrale de Nazinga", "Ruines de Loropéni", "Pics de Sindou", "Cascades de Karfiguéla", "Lac de Tengréla"]
    }

    print("🚀 Début de l'importation sécurisée...")

    # Insertion des circuits
    for nom, desc, jours in circuits_data:
        circuit, created = Circuit.objects.get_or_create(
            nom=nom,
            defaults={'description': desc, 'nb_jours': jours}
        )
        print(f"✅ {'Créé' if created else 'Déjà présent'} : {nom}")

    # Insertion des étapes
    for nom_circuit, noms_sites in circuits_etapes.items():
        try:
            circuit = Circuit.objects.get(nom=nom_circuit)
            for i, nom_site in enumerate(noms_sites):
                try:
                    site = SiteTouristique.objects.get(nom=nom_site)
                    CircuitEtape.objects.get_or_create(
                        circuit=circuit,
                        site=site,
                        defaults={'commentaire': f"Jour {i + 1} : {nom_site}"}
                    )
                except SiteTouristique.DoesNotExist:
                    print(f"  - ❌ Site '{nom_site}' introuvable (étape ignorée).")
        except Circuit.DoesNotExist:
            print(f"❌ Circuit '{nom_circuit}' introuvable.")

    print("\n✨ Importation terminée avec succès !")

if __name__ == "__main__":
    run()