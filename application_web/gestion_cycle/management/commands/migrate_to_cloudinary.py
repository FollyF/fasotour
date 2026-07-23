import cloudinary.uploader
from django.core.management.base import BaseCommand
from gestion_cycle.models import SiteImage, Guide

class Command(BaseCommand):
    help = "Migre les images locales existantes vers Cloudinary"

    def handle(self, *args, **options):
        for site_image in SiteImage.objects.all():
            if site_image.image and not str(site_image.image).startswith('http'):
                try:
                    local_path = site_image.image.path
                    result = cloudinary.uploader.upload(local_path)
                    site_image.image = result['public_id']
                    site_image.save()
                    self.stdout.write(self.style.SUCCESS(f"OK: {local_path}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erreur SiteImage {site_image.id}: {e}"))

        for guide in Guide.objects.all():
            if guide.photo and not str(guide.photo).startswith('http'):
                try:
                    local_path = guide.photo.path
                    result = cloudinary.uploader.upload(local_path)
                    guide.photo = result['public_id']
                    guide.save()
                    self.stdout.write(self.style.SUCCESS(f"OK: {local_path}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erreur Guide {guide.id}: {e}"))