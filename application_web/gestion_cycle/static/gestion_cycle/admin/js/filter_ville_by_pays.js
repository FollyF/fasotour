// votre_app/static/admin/js/filter_ville_by_pays.js
document.addEventListener('DOMContentLoaded', function() {
    function updateVilles() {
        const paysSelect = document.querySelector('#id_pays');
        const villeSelect = document.querySelector('#id_ville');
        
        if (!paysSelect || !villeSelect) return;
        
        const paysId = paysSelect.value;
        
        if (paysId) {
            fetch(`/admin/villes-by-pays/?pays_id=${paysId}`)
                .then(response => response.json())
                .then(data => {
                    villeSelect.innerHTML = '';
                    
                    // Option vide
                    const emptyOption = document.createElement('option');
                    emptyOption.value = '';
                    emptyOption.textContent = '---------';
                    villeSelect.appendChild(emptyOption);
                    
                    // Ajout des villes
                    data.forEach(ville => {
                        const option = document.createElement('option');
                        option.value = ville.id;
                        option.textContent = ville.nom;
                        if (villeSelect.dataset.selected == ville.id) {
                            option.selected = true;
                        }
                        villeSelect.appendChild(option);
                    });
                });
        } else {
            villeSelect.innerHTML = '<option value="">---------</option>';
        }
    }
    
    const paysSelect = document.querySelector('#id_pays');
    if (paysSelect) {
        paysSelect.addEventListener('change', updateVilles);
        
        // Pré-sélection si valeur existante
        if (paysSelect.value) {
            updateVilles();
        }
    }
    
    // Stocker la ville sélectionnée actuelle
    const villeSelect = document.querySelector('#id_ville');
    if (villeSelect) {
        villeSelect.dataset.selected = villeSelect.value;
    }
});