import sqlite3
import os

# --- Configuration de la base de données ---
# Assurez-vous que ce chemin est correct pour votre projet
DB_PATH = r'C:\DOCS\SEA\UJKZ\COURS\S5\PYTHON\PROJET\ApplicationWebAffichageHTML\application_web\db.sqlite3'

# --- Données des circuits et des étapes ---

# Données des circuits
circuits_data = [
    ("Circuit des Joyaux du Sahel",
     "Une aventure inoubliable à travers le désert, à la découverte des trésors cachés et des traditions nomades du nord du pays.",
     7),
    ("Sur la Route des Savanes",
     "Un voyage immersif au cœur des savanes, à la rencontre de la faune sauvage et des villages traditionnels de l'ouest burkinabè.",
     5),
    ("L'Épopée du Royaume Mossi",
     "Explorez l'histoire et la culture de l'ancien empire Mossi, de la capitale Ouagadougou aux villages des alentours.",
     3),
    ("Circuit des Cascadelles",
     "Une escapade rafraîchissante pour découvrir les cascades et les paysages luxuriants du sud-ouest, idéal pour les amateurs de nature.",
     4),
    ("Aventure Gourmande à Bobo",
     "Plongez dans l'ambiance unique de Bobo-Dioulasso et savourez la gastronomie locale tout en explorant ses sites emblématiques.",
     2),
    ("Circuit du Pays Lobi",
     "Découvrez l'architecture fortifiée et les coutumes fascinantes du peuple Lobi dans le sud-ouest du Burkina.", 3),
    ("Escapade au Pays Dogon",
     "Une incursion culturelle et spirituelle pour explorer les falaises, les grottes et les traditions ancestrales du peuple Dogon.",
     6),
    ("Les Trésors du Gourma",
     "Un circuit pour les passionnés d'histoire, d'art et de culture, à travers les sites historiques et les marchés de la région du Gourma.",
     5),
    ("Le Sentier des Artisans",
     "Une immersion dans l'artisanat burkinabè, de la poterie à la sculpture, en visitant les ateliers et les villages d'artistes.",
     4),
    ("Randonnée dans le Parc National d'Arly",
     "Un circuit pour les amoureux de la nature, avec des safaris, des randonnées et des observations d'animaux dans l'un des plus beaux parcs du pays.",
     2)
]

# Données des étapes de circuit
circuits_etapes = {
    "Circuit des Joyaux du Sahel": [
        "Musée National du Burkina Faso",
        "Village Artisanal de Ouagadougou (VAO)",
        "Site de sculptures de Laongo",
        "Vieilles Mosquées de Bani",
        "Réserve Naturelle Intégrale de Nazinga",
        "Cour Royale de Tiébélé",
        "Ruines de Loropéni"
    ],
    "Sur la Route des Savanes": [
        "Grande Mosquée de Dioulassoba",
        "Dômes de Fabédougou",
        "Cascades de Karfiguéla",
        "Lac de Tengréla",
        "Mare aux hippopotames"
    ],
    "L'Épopée du Royaume Mossi": [
        "Musée National du Burkina Faso",
        "Place de la Révolution",
        "Village Artisanal de Ouagadougou (VAO)",
        "Site de sculptures de Laongo",
        "Salon international de l'artisanat de Ouagadougou (SIAO)",
        "Festival panafricain du cinéma et de la télévision de Ouagadougou (FESPACO)"
    ],
    "Circuit des Cascadelles": [
        "Dômes de Fabédougou",
        "Lac de Tengréla",
        "Cascades de Karfiguéla",
        "Pics de Sindou",
        "Caverne de Douna"
    ],
    "Aventure Gourmande à Bobo": [
        "Grande Mosquée de Dioulassoba",
        "Mare aux hippopotames",
        "Dômes de Fabédougou",
        "Lac de Tengréla",
        "Cascades de Karfiguéla",
        "Pics de Sindou"
    ],
    "Circuit du Pays Lobi": [
        "Cour Royale de Tiébélé",
        "Réserve Naturelle Intégrale de Nazinga",
        "Ruines de Loropéni",
        "Pics de Sindou",
        "Caverne de Douna"
    ],
    "Escapade au Pays Dogon": [
        "Vieilles Mosquées de Bani",
        "Cour Royale de Tiébélé",
        "Ruines de Loropéni",
        "Pics de Sindou",
        "Caverne de Douna",
        "Grande Mosquée de Dioulassoba"
    ],
    "Les Trésors du Gourma": [
        "Musée National du Burkina Faso",
        "Village Artisanal de Ouagadougou (VAO)",
        "Réserve Naturelle Intégrale de Nazinga",
        "Cour Royale de Tiébélé",
        "Ruines de Loropéni",
        "Vieilles Mosquées de Bani"
    ],
    "Le Sentier des Artisans": [
        "Village Artisanal de Ouagadougou (VAO)",
        "Salon international de l'artisanat de Ouagadougou (SIAO)",
        "Musée National du Burkina Faso",
        "Site de sculptures de Laongo",
        "Grande Mosquée de Dioulassoba"
    ],
    "Randonnée dans le Parc National d'Arly": [
        "Réserve Naturelle Intégrale de Nazinga",
        "Ruines de Loropéni",
        "Pics de Sindou",
        "Cascades de Karfiguéla",
        "Lac de Tengréla"
    ]
}


def populate_db():
    """
    Connecte à la base de données et la peuple avec les données des circuits et des étapes.
    """
    if not os.path.exists(DB_PATH):
        print(f"Erreur : Le fichier de base de données '{DB_PATH}' n'existe pas.")
        print("Veuillez d'abord lancer 'python manage.py migrate' pour le créer.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("Connexion à la base de données réussie.")

        # Peuplement des circuits
        print("\n--- Insertion des circuits ---")
        for nom, description, nb_jours in circuits_data:
            try:
                # Vérifie si le circuit existe déjà pour éviter les doublons
                cursor.execute("SELECT id FROM gestion_cycle_circuit WHERE nom = ?", (nom,))
                result = cursor.fetchone()
                if result:
                    print(f"⚠️ Circuit '{nom}' existe déjà. Mise à jour des données.")
                    cursor.execute("UPDATE gestion_cycle_circuit SET description = ?, nb_jours = ? WHERE nom = ?",
                                   (description, nb_jours, nom))
                else:
                    cursor.execute("INSERT INTO gestion_cycle_circuit (nom, description, nb_jours) VALUES (?, ?, ?)",
                                   (nom, description, nb_jours))
                    print(f"✅ Circuit '{nom}' inséré.")
                conn.commit()
            except sqlite3.IntegrityError as e:
                print(f"Erreur d'intégrité lors de l'insertion du circuit '{nom}': {e}")
            except Exception as e:
                print(f"Erreur inattendue lors de l'insertion du circuit '{nom}': {e}")

        # Peuplement des étapes
        print("\n--- Insertion des étapes de circuit ---")
        for nom_circuit, noms_etapes in circuits_etapes.items():
            try:
                cursor.execute("SELECT id FROM gestion_cycle_circuit WHERE nom = ?", (nom_circuit,))
                circuit_id = cursor.fetchone()[0]
                print(f"\nAjout des étapes pour le circuit : '{nom_circuit}' (ID: {circuit_id})")

                for ordre, nom_site in enumerate(noms_etapes):
                    try:
                        cursor.execute("SELECT id FROM gestion_cycle_sitetouristique WHERE nom = ?", (nom_site,))
                        site_id = cursor.fetchone()[0]

                        # Vérifie si l'étape existe déjà
                        cursor.execute("SELECT 1 FROM gestion_cycle_circuitetape WHERE circuit_id = ? AND site_id = ?",
                                       (circuit_id, site_id))
                        if cursor.fetchone():
                            print(f"  - Étape '{nom_site}' existe déjà. Passé.")
                            continue

                        commentaire = f"Jour {ordre + 1} : {nom_site}"
                        cursor.execute(
                            "INSERT INTO gestion_cycle_circuitetape (circuit_id, site_id, commentaire) VALUES (?, ?, ?)",
                            (circuit_id, site_id, commentaire))
                        print(f"  - Étape '{nom_site}' ajoutée.")
                        conn.commit()

                    except TypeError:
                        print(f"  - ❌ ERREUR : Site touristique '{nom_site}' non trouvé.")
                    except sqlite3.IntegrityError as e:
                        print(f"  - Erreur d'intégrité lors de l'ajout de l'étape '{nom_site}': {e}")
                    except Exception as e:
                        print(f"  - Erreur inattendue lors de l'ajout de l'étape '{nom_site}': {e}")

            except TypeError:
                print(
                    f"❌ ERREUR : Circuit '{nom_circuit}' non trouvé dans la base de données. Les étapes ne peuvent pas être ajoutées.")
            except Exception as e:
                print(f"❌ ERREUR inattendue lors du traitement du circuit '{nom_circuit}': {e}")

    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
    finally:
        if conn:
            conn.close()
            print("\nConnexion à la base de données fermée.")


if __name__ == "__main__":
    populate_db()