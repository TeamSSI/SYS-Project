#!/usr/bin/python3

from flask import Flask, jsonify, request
from flask_cors import CORS
import platform
import psutil
import os
import subprocess
import socket
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Fonction pour obtenir les informations système
def obtenir_infos_systeme():
    return {
        "système": platform.system(),
        "version": platform.version(),
        "release": platform.release(),
        "processeur": platform.processor(),
        "architecture": platform.architecture()[0]
    }

# Fonction pour obtenir les informations de la mémoire
def obtenir_infos_memoire():
    memoire = psutil.virtual_memory()
    disque = psutil.disk_usage('/')
    return {
        "mémoire_totale_RAM (octets)": memoire.total,
        "mémoire_disponible_RAM (octets)": memoire.available,
        "mémoire_utilisée_RAM (octets)": memoire.used,
        "pourcentage_mémoire_RAM (%)": memoire.percent,
        "disque_total (octets)": disque.total,
        "disque_utilisé (octets)": disque.used,
        "espace_libre_disque (octets)": disque.free,
        "pourcentage_disque (%)": disque.percent
    }

# Fonction pour obtenir les informations de la batterie
def obtenir_infos_batterie():
    try:
        batterie = psutil.sensors_battery()
        if batterie:
            return {
                "niveau_batterie (%)": batterie.percent,
                "branché": batterie.power_plugged,
                "temps_restant (minutes)": batterie.secsleft // 60 if batterie.secsleft != psutil.POWER_TIME_UNLIMITED else "Inconnu"
            }
        else:
            return {"erreur": "Aucune information sur la batterie disponible"}
    except Exception as e:
        return {"erreur": str(e)}

# Fonction pour obtenir les informations sur les périphériques
def obtenir_infos_peripheriques():
    try:
        if os.name == 'posix':
            peripheriques = subprocess.check_output('lsusb', shell=True).decode()
        elif os.name == 'nt':
            peripheriques = subprocess.check_output('wmic path Win32_USBControllerDevice get Dependent', shell=True).decode()
        else:
            peripheriques = "OS non supporté pour cette fonctionnalité"
        return {"périphériques": peripheriques}
    except Exception as e:
        return {"erreur": str(e)}

# Fonction pour obtenir les informations CPU
def obtenir_infos_cpu():
    return {
        "nom_cpu": platform.processor(),
        "coeurs_physiques": psutil.cpu_count(logical=False),
        "coeurs_logiques": psutil.cpu_count(logical=True),
        "utilisation_cpu (%)": psutil.cpu_percent(interval=1)
    }

# Routes de l'API
@app.route('/')
def principale():
    return "<p>azzedin za3Im</p>"

@app.route('/infos_systeme', methods=['GET'])
def infos_systeme():
    return jsonify(obtenir_infos_systeme())

@app.route('/infos_memoire', methods=['GET'])
def infos_memoire():
    return jsonify(obtenir_infos_memoire())

@app.route('/infos_batterie', methods=['GET'])
def infos_batterie():
    return jsonify(obtenir_infos_batterie())

@app.route('/infos_peripheriques', methods=['GET'])
def infos_peripheriques():
    return jsonify(obtenir_infos_peripheriques())

@app.route('/infos_cpu', methods=['GET'])
def infos_cpu():
    return jsonify(obtenir_infos_cpu())

@app.route('/demarrer_serveur', methods=['POST'])
def demarrer_serveur():

    adresse_ip = request.json.get('ip')
    port = request.json.get('port')
    
    if not adresse_ip or not port:
        return jsonify({'erreur': 'IP et port requis'}), 400

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((adresse_ip, int(port)))
        s.listen(5)
        print("En attente de connexion...")

        cible, ip = s.accept()
        print(f"Connecté à {ip}")

        donnees = recevoir(cible)
        s.close()

        return jsonify({'infos_systeme': donnees}), 200
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500

def recevoir(cible):
    json_data = ""
    while True:
        try:
            morceau = cible.recv(4096).decode()
            if not morceau:
                break
            json_data += morceau
            return json.loads(json_data)
        except json.JSONDecodeError:
            continue
    return {}

# Exécution principale du script
if __name__ == "__main__":
    app.run(debug=True)
