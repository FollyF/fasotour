from django.contrib import admin
from django.apps import apps

app_models = apps.get_app_config('gestion_cycle').get_models()

for model in app_models:
    list_display = []
    list_filter = []
    search_fields = []

    # Préparer list_display et list_filter
    for field in model._meta.get_fields():
        if field.many_to_many:
            # Pour les ManyToManyField, créer une méthode dynamique
            def make_m2m_display(f):
                return lambda obj: ", ".join([str(x) for x in getattr(obj, f.name).all()])
            method_name = f"display_{field.name}"
            setattr(model, method_name, make_m2m_display(field))
            list_display.append(method_name)
        elif field.one_to_many:
            continue  # Ignorer les reverse relations
        elif field.get_internal_type() == 'ForeignKey':
            # Afficher la ForeignKey via son __str__()
            def make_fk_display(f):
                return lambda obj: getattr(obj, f.name)
            method_name = f"display_{field.name}"
            setattr(model, method_name, make_fk_display(field))
            list_display.append(method_name)
            list_filter.append(field.name)
        else:
            list_display.append(field.name)
            if field.get_internal_type() in ['BooleanField']:
                list_filter.append(field.name)
            if field.get_internal_type() in ['CharField', 'TextField']:
                search_fields.append(field.name)

    # Créer le ModelAdmin dynamique
    class AutoAdmin(admin.ModelAdmin):
        list_display = list_display
        list_filter = list_filter
        search_fields = search_fields

    # Enregistrer le modèle
    try:
        admin.site.register(model, AutoAdmin)
    except admin.sites.AlreadyRegistered:
        pass
