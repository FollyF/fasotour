import sqlite3
import os

# Remplacer 'db.sqlite3' par le nom de votre fichier de base de données
DB_PATH = r'C:\DOCS\SEA\UJKZ\COURS\S5\PYTHON\PROJET\ApplicationWebAffichageHTML\application_web\db.sqlite3'
# Vérifier si le fichier de la base de données existe
if not os.path.exists(DB_PATH):
    print(f"Erreur : Le fichier de base de données {DB_PATH} n'existe pas.")
    exit()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

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

# Nom de la table. Elle suit généralement le format appname_modelname.
# Dans votre cas, ce sera gestion_cycle_circuit
table_name = "gestion_cycle_circuit"

try:
    # Exécuter une requête pour chaque circuit
    for circuit in circuits_data:
        sql = f"INSERT INTO {table_name} (nom, description, nb_jours) VALUES (?, ?, ?)"
        cursor.execute(sql, circuit)

    conn.commit()
    print("10 circuits ont été insérés avec succès.")

except sqlite3.Error as e:
    print(f"Une erreur s'est produite : {e}")
    conn.rollback()

finally:
    conn.close()