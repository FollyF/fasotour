# docker compose exec web python scripts/indexer_images.py

import os
import sys
import django

# Configuration standard
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application_web.settings")
django.setup()

from gestion_cycle.models import SiteTouristique, SiteImage

def indexer():
    # Ciblez le dossier où Django stocke vos images (adapter selon votre MEDIA_ROOT)
    # Généralement dans votre projet c'est 'gestion_cycle/media/site_images'
    base_media = os.path.join(project_root, 'gestion_cycle', 'media', 'site_images')

    for nom_dossier in os.listdir(base_media):
        dossier_site = os.path.join(base_media, nom_dossier)
        
        if not os.path.isdir(dossier_site):
            continue

        # Essayer de trouver le site correspondant au nom du dossier
        nom_site = nom_dossier.replace('_', ' ')
        site = SiteTouristique.objects.filter(nom__iexact=nom_site).first()

        if not site:
            print(f"⚠️ Site non trouvé pour le dossier : {nom_dossier}")
            continue

        # Parcourir les images dans le dossier
        for fichier in os.listdir(dossier_site):
            if not fichier.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue  # Ignorer les fichiers non image
            
            nom_sans_ext = os.path.splitext(fichier)[0]
            if not nom_sans_ext.isdigit():
                print(f"⚠️ Nom de fichier non conforme (doit être un nombre) : {fichier} dans {nom_dossier}")
                continue    
            
            ordre = int(nom_sans_ext)
            # Chemin relatif pour la base de données
            image_path = f"site_images/{nom_dossier}/{fichier}"
            
            # Vérifier si c'est déjà en base (évite les doublons)
            if not SiteImage.objects.filter(image=image_path).exists():
                # Création de l'objet : Django gère le lien avec le fichier déjà présent
                SiteImage.objects.create(
                    site=site,
                    image=image_path,
                    ordre=ordre
                )
                print(f"✅ Indexé : {image_path} pour {site.nom}")
            else:
                print(f"⏭️  Déjà indexé : {image_path}")

if __name__ == "__main__":
    indexer()