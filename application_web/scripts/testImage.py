import os
import sys
import json
import django

# --- 1. CONFIGURATION ROBUSTE DU CHEMIN ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application_web.settings')
django.setup()

from django.conf import settings

def tester_et_valider_images(nom_fichier_json):
    """
    Valide l'existence des fichiers images listés dans le JSON via settings.MEDIA_ROOT
    """
    # Utilisation de settings.BASE_DIR ou équivalent pour localiser le JSON
    chemin_fichier_json = os.path.join(project_root, 'gestion_cycle', 'fixtures', nom_fichier_json)
    
    # Utilisation de la configuration réelle de Django pour le dossier media
    media_root = settings.MEDIA_ROOT

    if not os.path.exists(chemin_fichier_json):
        print(f"❌ Erreur : Le fichier '{chemin_fichier_json}' n'a pas été trouvé.")
        return

    try:
        with open(chemin_fichier_json, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Erreur : Le fichier JSON est invalide : {e}")
        return

    print(f"🔍 Début du test sur {len(donnees)} entrées...")

    images_manquantes = 0
    erreurs_json = 0

    for i, entree in enumerate(donnees):
        try:
            # On cherche soit dans 'fields', soit directement si c'est un format simple
            champs = entree.get('fields', entree)
            image_path = champs.get('image')

            if not image_path:
                continue

            # Vérification via le chemin absolu configuré dans Django
            chemin_complet = os.path.join(media_root, str(image_path).lstrip('/'))
            
            if not os.path.exists(chemin_complet):
                print(f"❌ Image manquante (Entrée {i+1}) : '{image_path}'")
                images_manquantes += 1

        except Exception as e:
            print(f"❌ Erreur sur l'entrée {i+1} : {e}")
            erreurs_json += 1

    print("\n--- Résultat du test ---")
    print(f"Total entrées : {len(donnees)} | Manquantes : {images_manquantes} | Erreurs JSON : {erreurs_json}")

    if images_manquantes == 0 and erreurs_json == 0:
        print("\n✅ Tout est prêt ! Vous pouvez importer vos données en toute sécurité.")
    else:
        print("\n❌ Test échoué. Corrigez les images listées ci-dessus.")

if __name__ == "__main__":
    tester_et_valider_images("site_images.json")