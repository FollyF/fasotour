import os
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from gestion_cycle.models import SiteImage, Guide

class Command(BaseCommand):
    help = "Corrige les SiteImage cassées après une migration Cloudinary ratée"

    def handle(self, *args, **options):
        media_root = os.path.join(settings.BASE_DIR, "gestion_cycle", "media")
        extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.PNG', '.JPEG']

        fixed = 0
        errors = 0

        for si in SiteImage.objects.all():
            current_name = str(si.image.name)
            if "/" not in current_name:
                folder_name = si.site.nom.replace(" ", "_")
                found_path = None

                for ext in extensions:
                    candidate = os.path.join(
                        media_root, "site_images", folder_name, f"{si.ordre}{ext}"
                    )
                    if os.path.exists(candidate):
                        found_path = candidate
                        break

                if found_path:
                    try:
                        filename = os.path.basename(found_path)
                        with open(found_path, 'rb') as f:
                            si.image.save(filename, File(f), save=True)
                        self.stdout.write(self.style.SUCCESS(f"OK id={si.id}: {found_path}"))
                        fixed += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur id={si.id}: {e}"))
                        errors += 1
                else:
                    self.stdout.write(self.style.WARNING(f"Fichier introuvable id={si.id} (site={folder_name}, ordre={si.ordre})"))
                    errors += 1

        self.stdout.write(self.style.SUCCESS(f"\nTerminé — {fixed} corrigées, {errors} erreurs/manquantes"))