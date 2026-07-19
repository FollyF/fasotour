from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import folium
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', "scripts"))
from scripts.folium_utils import folium_to_png
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings

import cloudinary.uploader

def folium_to_png(map_obj, filename="circuit_preview.png"):
    temp_html = os.path.join(settings.BASE_DIR, "temp_map.html")
    map_obj.save(temp_html)

    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(600, 400)
    driver.get("file://" + temp_html)
    time.sleep(2)

    # Sauvegarde temporaire locale (juste le temps de l'upload)
    temp_png = os.path.join(settings.BASE_DIR, filename)
    driver.save_screenshot(temp_png)
    driver.quit()
    os.remove(temp_html)

    # Upload vers Cloudinary
    result = cloudinary.uploader.upload(temp_png, public_id=f"maps/{filename}")
    os.remove(temp_png)  # nettoie le fichier temporaire local

    return result["secure_url"]  # URL Cloudinary complète, utilisable directement

def site_image_upload_path(instance, filename):
    return f'site_images/{instance.site.nom.replace(" ", "_")}/{filename}'

class Ville(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, default="Burkina Faso")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    code_iso2 = models.CharField(max_length=2, default="BF")
    region = models.CharField(max_length=100, null=True, blank=True)
    statut = models.CharField(max_length=50, null=True, blank=True)
    population = models.BigIntegerField(null=True, blank=True)
    population_propre = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.region})"

class CategorieSite(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class SiteTouristique(models.Model):
    nom = models.CharField(max_length=150)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='sites')
    description = models.TextField(blank=True, null=True)
    site_web = models.URLField(blank=True, null=True, default="ontb.bf")
    categorie = models.ForeignKey(CategorieSite, on_delete=models.SET_NULL, blank=True, null=True, related_name='sites')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    tarif = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    horaire = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nom} ({self.ville.nom})"

class SiteImage(models.Model):
    site = models.ForeignKey(SiteTouristique, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=site_image_upload_path)
    ordre = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['ordre']

class Guide(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    photo = models.ImageField(upload_to='guides/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"



class Circuit(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    nb_jours = models.IntegerField(default=1)
    guide = models.ForeignKey(
        Guide, on_delete=models.SET_NULL, null=True, blank=True, related_name="circuits"
    )
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    map_url = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.nom

@receiver(post_save, sender=Circuit)
def generate_circuit_png(sender, instance, created, **kwargs):
    """
    Génère automatiquement un PNG miniature pour chaque nouveau circuit.
    """
    if created:
        etapes = instance.etapes.all()
        if not etapes.exists():
            return

        first_site = etapes.first().site
        m = folium.Map(location=[first_site.latitude, first_site.longitude],
                       zoom_start=6, width=600, height=400)

        for etape in etapes:
            site = etape.site
            if site.latitude and site.longitude:
                folium.Marker(
                    location=[site.latitude, site.longitude],
                    popup=site.nom,
                    tooltip=site.nom,
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)

        # Nom du PNG
        map_filename = f"circuit_{instance.id}.png"

        # Générer le PNG et mettre à jour map_url
        instance.map_url = folium_to_png(m, map_filename)
        instance.save(update_fields=["map_url"])



class CircuitEtape(models.Model):
    circuit = models.ForeignKey(
        Circuit, on_delete=models.CASCADE, related_name="etapes"
    )
    site = models.ForeignKey(
        SiteTouristique, on_delete=models.CASCADE
    )
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['circuit', 'site'], name='unique_site_per_circuit')
        ]

    def __str__(self):
        return f"{self.circuit.nom} - {self.site.nom}"


class Reservation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    circuit = models.ForeignKey(CircuitEtape, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(default=timezone.now)
    nombre_personnes = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.circuit.nom}"