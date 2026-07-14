import os, time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from django.conf import settings

def folium_to_png(map_obj, filename="circuit_preview.png", width=600, height=400):
    """
    Génère un PNG statique à partir d'une carte Folium.
    width et height définissent la taille du rendu.
    Retourne le chemin relatif pour {% static %}.
    """

    # 1️⃣ Sauvegarde temporaire en HTML
    temp_html = os.path.join(settings.BASE_DIR, "temp_map.html")
    map_obj.save(temp_html)

    # 2️⃣ Configurer Firefox headless
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # 3️⃣ Ouvrir le HTML et définir la taille du rendu
    driver.set_window_size(width, height)
    driver.get("file://" + temp_html)

    # 4️⃣ Attendre que la carte se charge complètement
    time.sleep(2)

    # 5️⃣ Sauvegarder le screenshot dans static/maps/
    output_dir = os.path.join(settings.BASE_DIR, "gestion_cycle", "static", "maps")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    driver.save_screenshot(output_path)

    # 6️⃣ Fermer le navigateur et supprimer le HTML temporaire
    driver.quit()
    os.remove(temp_html)

    # 7️⃣ Retourner le chemin relatif pour utiliser dans le template
    return f"maps/{filename}"
