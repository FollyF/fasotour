import math
import os

import folium
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from scripts.folium_utils import folium_to_png


# Connexion
def connexion(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_url = request.POST.get("next")  # récupération du "next"

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Rediriger vers la page demandée ou home si next est vide
            return redirect(next_url if next_url else "home")
        else:
            messages.error(request, "Email ou mot de passe incorrect.")

    # On récupère "next" si l'utilisateur a été redirigé automatiquement
    next_url = request.GET.get("next", "")
    return render(request, "gestion_cycle/connexion.html", {"next": next_url})

def deconnexion(request):
    logout(request)
    return redirect('home')

# Inscription
def inscription(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next')  # récupère l'URL de redirection après inscription

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d’utilisateur existe déjà.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect(next_url or 'home')  # redirige vers la réservation ou home

    return render(request, 'gestion_cycle/inscription.html')


# Déconnexion
def deconnexion(request):
    logout(request)
    return redirect('home')


# Réserver un circuit
@login_required(login_url='connexion')
def reserver_circuit(request, circuit_id):
    circuit = get_object_or_404(Circuit, pk=circuit_id)
    if request.method == "POST":
        nombre = int(request.POST.get("nombre_personnes", 1))
        Reservation.objects.create(
            utilisateur=request.user,
            circuit=circuit,
            nombre_personnes=nombre
        )
        messages.success(request, f"Réservation pour {circuit.nom} enregistrée !")
        return redirect('mes_reservations')
    return render(request, "gestion_cycle/reserver_circuit.html", {"circuit": circuit})


# Liste des réservations de l'utilisateur
@login_required
def mes_reservations(request):
    reservations = Reservation.objects.filter(utilisateur=request.user)
    return render(request, "gestion_cycle/mes_reservations.html", {"reservations": reservations})


# Page d'accueil
def home(request):
    return render(request, 'gestion_cycle/home.html')


def sites_touristiques(request):
    sites = SiteTouristique.objects.all()
    return render(request, 'gestion_cycle/sites_touristiques.html', {'sites': sites})


def detail_site(request, site_id):
    site = get_object_or_404(SiteTouristique, pk=site_id)
    burkina_center = [12.2383, -1.5616]
    site_coord = [float(site.latitude), float(site.longitude)]

    card = folium.Map(location=burkina_center, zoom_start=7, min_zoom=7, max_zoom=7)

    folium.Marker(
        site_coord,
        popup=site.nom,
        tooltip=site.ville,
        icon=folium.Icon(color='red', icon='monument', prefix='fa')
    ).add_to(card)

    card_html = card._repr_html_()
    return render(request, 'gestion_cycle/detail_site_touristique.html', {'site': site, 'card_html': mark_safe(card_html)})


def circuits(request):
    circuits = Circuit.objects.all()
    output_dir = os.path.join(settings.BASE_DIR, "gestion_cycle", "static", "maps")
    os.makedirs(output_dir, exist_ok=True)

    for circuit in circuits:
        etapes = CircuitEtape.objects.filter(circuit=circuit).select_related("site")

        if etapes.exists():
            first_site = etapes.first().site
            card_width, card_height = 600, 400
            m = folium.Map(
                location=[first_site.latitude, first_site.longitude],
                zoom_start=6,
                width=card_width,
                height=card_height
            )

            for etape in etapes:
                site = etape.site
                if site.latitude and site.longitude:
                    folium.Marker(
                        location=[float(site.latitude), float(site.longitude)],
                        popup=site.nom,
                        tooltip=site.nom,
                        icon=folium.Icon(color="red", icon="info-sign")
                    ).add_to(m)

            map_filename = f"circuit_{circuit.id}.png"
            map_path = os.path.join(output_dir, map_filename)

            if not os.path.exists(map_path):
                circuit.map_url = folium_to_png(m, map_filename)
            else:
                circuit.map_url = f"maps/{map_filename}"

        else:
            circuit.map_url = None

    return render(request, "gestion_cycle/circuits.html", {"circuits": circuits})


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def detail_circuit(request, circuit_id):
    circuit = get_object_or_404(Circuit, pk=circuit_id)
    aero_ouaga = (12.3532, -1.51242, "Aéroport d'Ouagadougou", "Point de départ et d'arrivée du circuit.")

    etapes = circuit.etapes.all()
    sites = [etape.site for etape in etapes]

    points = [(float(site.latitude), float(site.longitude), site.nom, site.description) for site in sites]
    optimized_tour = [aero_ouaga]
    remaining_points = list(points)

    while remaining_points:
        current_lat, current_lon, _, _ = optimized_tour[-1]
        closest_point = min(remaining_points, key=lambda p: haversine(current_lat, current_lon, p[0], p[1]))
        optimized_tour.append(closest_point)
        remaining_points.remove(closest_point)

    final_tour = optimized_tour + [aero_ouaga]

    m = folium.Map(location=[aero_ouaga[0], aero_ouaga[1]], zoom_start=7, min_zoom=7, max_zoom=8)

    for i, (lat, lon, name, description) in enumerate(final_tour):
        day_number = i + 1
        icon_html = f"""
            <div style="
                background-color: #0d6efd;
                color: white;
                border-radius: 50%;
                width: 25px;
                height: 25px;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid white;
                box-shadow: 0 0 5px rgba(0,0,0,0.5);
            ">{day_number}</div>
        """
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{name}</b><br>{description}",
            tooltip=name,
            icon=folium.DivIcon(html=icon_html)
        ).add_to(m)

    tour_locations = [(p[0], p[1]) for p in final_tour]
    folium.PolyLine(locations=tour_locations, color="red", weight=2).add_to(m)

    map_html = m._repr_html_()

    return render(request, "gestion_cycle/detail_circuit.html", {
        "circuit": circuit,
        "final_tour": final_tour,
        "map_html": mark_safe(map_html),
    })
