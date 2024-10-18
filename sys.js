document.addEventListener('DOMContentLoaded', () => {
    const bLocal = document.getElementById('b-local');
    const infoLocal = document.querySelector('.info-local');
    const buttonHolder = document.getElementById('button_holder');
    const button_ret =document.getElementById('ret');
    // Cacher la section des informations locales au démarrage
    infoLocal.style.display = 'none';
    button_ret.style.display = 'none';

    // Afficher les informations locales et masquer les boutons lorsque l'on clique sur b-local
    bLocal.addEventListener('click', () => {
        buttonHolder.style.display = 'none'; // Masque les boutons
        infoLocal.style.display = 'block'; // Affiche les informations locales
        button_ret.style.display = 'block';
        button_ret.style.backgroundColor='red';
        button_ret.style.color='white';
        // Charger les informations système après le clic sur le bouton
        fetchData('system_info', 'system-info');
        fetchData('memory_info', 'memory-info');
        fetchData('cpu_info', 'cpu-info');
        fetchData('peripheral_info', 'peripheral-info');
        fetchData('battery_info', 'battery-info');
    });

    button_ret.addEventListener('click', ()=>{
         buttonHolder.style.display = 'grid'; // Masque les boutons
        infoLocal.style.display = 'none'; // Affiche les informations locales
        button_ret.style.display = 'none';
    })
});

// Fonction pour récupérer les données via l'API et les afficher
const fetchData = (endpoint, elementId) => {
    fetch(`http://127.0.0.1:5000/${endpoint}`)
        .then(response => response.json())
        .then(data => {
            const element = document.getElementById(elementId);
            element.innerHTML = ""; // Vider le contenu précédent

            // Remplir les informations dans une liste
            for (const [key, value] of Object.entries(data)) {
                const li = document.createElement('li');
                if (typeof value === 'object' && !Array.isArray(value)) {
                    // Si la valeur est un objet, afficher ses propriétés
                    li.textContent = key + ":";
                    const nestedUl = document.createElement('ul');
                    for (const [nestedKey, nestedValue] of Object.entries(value)) {
                        const nestedLi = document.createElement('li');
                        nestedLi.textContent = `${nestedKey.replace(/_/g, ' ')}: ${nestedValue}`;
                        nestedUl.appendChild(nestedLi);
                    }
                    li.appendChild(nestedUl);
                } else {
                    // Sinon, afficher directement la valeur
                    li.textContent = `${key.replace(/_/g, ' ')}: ${value}`;
                }
                element.appendChild(li);
            }
        })
        .catch(error => console.error('Erreur:', error));
};
