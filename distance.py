#!/usr/bin/python3

from flask import Flask, request, render_template, jsonify
import socket
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})


@app.route('/start_server', methods=['POST'])
def start_server():
    ip_address = request.json.get('ip')
    port = request.json.get('port')

    if not ip_address or not port:
        return jsonify({'error': 'IP et port requis'}), 400

    # Lancer le serveur en utilisant les informations fournies
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip_address, int(port)))
        s.listen(5)
        print("En attente de connexion...")

        target, ip = s.accept()
        print(f"Connecté à {ip}")

        # Recevoir les informations du système du client
        data = receive(target)
        s.close()

        return jsonify({'system_info': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def receive(target):
    json_data = ""
    while True:
        try:
            chunk = target.recv(4096).decode()
            if not chunk:
                break
            json_data += chunk

            # Décoder les données JSON
            return json.loads(json_data)
        except json.JSONDecodeError:
            continue
    return {}


# Exécution principale du script
if __name__ == "__main__":
    app.run(debug=True)

