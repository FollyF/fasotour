from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cycle', '0002_alter_ville_nom'),  # dernière migration appliquée
    ]

    operations = [
        # Supprimer uniquement les anciens modèles
        migrations.DeleteModel(
            name='Circuit',
        ),
        migrations.DeleteModel(
            name='EtapeCircuit',
        ),
    ]
