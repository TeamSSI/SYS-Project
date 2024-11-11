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
        fetchData('infos_systeme', 'system-info');
        fetchData('infos_memoire', 'memory-info');
        fetchData('infos_cpu', 'cpu-info');
        fetchData('infos_peripheriques', 'peripheral-info');
        fetchData('infos_batterie', 'battery-info');
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
            console.log(data);
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


const buttonHolder = document.getElementById('button_holder');
const b_distance = document.getElementById('b-distance');
const form = document.getElementById('inp_form');
const button_ret = document.getElementById('ret');
const lancer = document.getElementById('Lancer');

form.style.display = "none";

// Afficher le formulaire lorsque le bouton b_distance est cliqué
b_distance.addEventListener('click', () => {
    buttonHolder.style.display = 'none';
    form.style.display = "block";
});

document.getElementById("Lancer").addEventListener("click", function(event) {
    event.preventDefault();
    
    const ip = document.getElementById("ip").value;
    const port = document.getElementById("port").value;



    console.log(ip)
    console.log(port)

    fetch("http://127.0.0.1:5000/demarrer_serveur", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ ip: ip, port: port })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Erreur :" + data.error);
        } else {
            console.log(data)
            displaySystemInfo(data.infos_systeme);
        }
    })
    .catch(error => {
        console.error("Erreur lors de la requête :", error);
    });
});

function displaySystemInfo(info) {
    const systemInfoList = document.getElementById("system-info2");
    systemInfoList.innerHTML = ""; // Clear previous data if any

    for (const key in info) {
        const item = document.createElement("li");
        item.className = "info-item"; // Adding a CSS class

        if (typeof info[key] === "object") {
            item.innerHTML = `<strong>${key}:</strong>`;
            const sublist = document.createElement("ul");
            sublist.className = "sublist"; // CSS class for nested lists
            for (const subKey in info[key]) {
                const subItem = document.createElement("li");
                subItem.className = "sublist-item"; // CSS class for sub-items
                subItem.textContent = `${subKey}: ${info[key][subKey]}`;
                sublist.appendChild(subItem);
            }
            item.appendChild(sublist);
        } else {
            item.innerHTML = `<strong>${key}:</strong> ${info[key]}`;
        }

        systemInfoList.appendChild(item);
    }
}




