import os
import sys
import django

# Permet au script de trouver le projet Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application_web.settings')
django.setup()

from gestion_cycle.models import Circuit, generate_circuit_png

def main():
    circuits = Circuit.objects.all()
    for circuit in circuits:
        print(f"Régénération pour : {circuit.nom}")
        try:
            generate_circuit_png(sender=Circuit, instance=circuit, created=True)
            print(f"OK: {circuit.nom}")
        except Exception as e:
            print(f"Erreur {circuit.nom}: {e}")

if __name__ == "__main__":
    main()