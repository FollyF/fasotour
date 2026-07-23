import os
import unicodedata
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from gestion_cycle.models import Guide

def normalize(text):
    """Retire les accents et met en minuscules, comme dans les noms de fichiers."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text.lower().replace(" ", "_").replace("-", "_")

class Command(BaseCommand):
    help = "Corrige les Guide.photo cassées après une migration Cloudinary ratée"

    def handle(self, *args, **options):
        guides_dir = os.path.join(settings.BASE_DIR, "gestion_cycle", "media", "guides")
        fixed = 0
        errors = 0

        for g in Guide.objects.all():
            current_name = str(g.photo.name) if g.photo else ""
            if current_name and "/" not in current_name:
                prenom_norm = normalize(g.prenom)
                nom_norm = normalize(g.nom)
                expected_filename = f"{prenom_norm}_{nom_norm}.jpg"
                expected_path = os.path.join(guides_dir, expected_filename)

                if os.path.exists(expected_path):
                    try:
                        with open(expected_path, 'rb') as f:
                            g.photo.save(expected_filename, File(f), save=True)
                        self.stdout.write(self.style.SUCCESS(f"OK id={g.id} ({g.prenom} {g.nom}): {expected_path}"))
                        fixed += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur id={g.id}: {e}"))
                        errors += 1
                else:
                    self.stdout.write(self.style.WARNING(f"Introuvable id={g.id} ({g.prenom} {g.nom}): {expected_path}"))
                    errors += 1

        self.stdout.write(self.style.SUCCESS(f"\nTerminé — {fixed} corrigées, {errors} erreurs/manquantes"))