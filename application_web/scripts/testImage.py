import os
import sys
import json

# --- Configuration de l'environnement Django ---
chemin_du_script = os.path.dirname(os.path.abspath(__file__))
chemin_racine_projet = os.path.dirname(chemin_du_script)
sys.path.append(chemin_racine_projet)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application_web.settings')

try:
    import django

    django.setup()
    from gestion_cycle.models import SiteTouristique, SiteImage
except Exception as e:
    print(f"Erreur lors de la configuration de l'environnement Django : {e}")
    sys.exit(1)


def tester_et_valider_images(nom_fichier_json):
    """
    Lit un fichier JSON, valide sa structure et vérifie l'existence des fichiers images.
    """
    # Chemin vers le fichier JSON dans le dossier 'fixtures' de l'application 'gestion_cycle'
    chemin_fichier_json = os.path.join(
        chemin_racine_projet, 'gestion_cycle', 'fixtures', nom_fichier_json
    )

    # Chemin vers le dossier media
    media_root = os.path.join(chemin_racine_projet, 'media')

    if not os.path.exists(chemin_fichier_json):
        print(f"Erreur : Le fichier '{chemin_fichier_json}' n'a pas été trouvé. 😔")
        return

    try:
        with open(chemin_fichier_json, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Erreur : Le fichier JSON est invalide. Détails : {e}")
        return

    print("--- Début du test des données JSON et des fichiers images ---")

    erreurs_validation_json = 0
    images_manquantes = 0
    total_entrees = len(donnees)

    for i, entree in enumerate(donnees):
        try:
            champs = entree['fields']
            image_path = champs['image']

            # Vérification de l'existence du fichier image
            chemin_complet_image = os.path.join(media_root, image_path)
            if not os.path.exists(chemin_complet_image):
                print(
                    f"❌ Erreur : L'image '{image_path}' pour l'entrée #{i + 1} est manquante. Chemin attendu : '{chemin_complet_image}'")
                images_manquantes += 1

        except (KeyError, ValueError, IndexError) as e:
            print(f"❌ Erreur de validation de la structure JSON à l'entrée #{i + 1} : {e}")
            erreurs_validation_json += 1

    print("\n--- Résultat du test ---")
    print(f"Total des entrées JSON : {total_entrees}")
    print(f"Nombre de fichiers images manquants : {images_manquantes}")
    print(f"Erreurs de structure JSON : {erreurs_validation_json}")

    if images_manquantes == 0 and erreurs_validation_json == 0:
        print("\n--- ✅ Tout est prêt ! Vous pouvez lancer 'loaddata' sans risque. ---")
    else:
        print("\n--- ❌ Test échoué. Veuillez corriger les problèmes listés ci-dessus avant de continuer. ---")


if __name__ == "__main__":
    tester_et_valider_images("site_images.json")