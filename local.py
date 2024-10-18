#!/usr/bin/python3

from flask import Flask, jsonify
from flask_cors import CORS
import platform
import psutil
import os
import subprocess


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Fonction pour obtenir les informations système
def get_system_info():
    return {
        "system": platform.system(),
        "version": platform.version(),
        "release": platform.release(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0]
    }

# Fonction pour obtenir les informations de la mémoire
def get_memory_info():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "total_memory_RAM (bytes)": memory.total,
        "available_memory_RAM (bytes)": memory.available,
        "used_memory_RAM (bytes)": memory.used,
        "memory_percentage_RAM (%)": memory.percent,
        "total_disk (bytes)": disk.total,
        "used_disk (bytes)": disk.used,
        "free_disk (bytes)": disk.free,
        "disk_percentage (%)": disk.percent
    }

# Fonction pour obtenir les informations de la batterie
def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "battery_level (%)": battery.percent,
                "plugged_in": battery.power_plugged,
                "time_left (minutes)": battery.secsleft // 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Inconnu"
            }
        else:
            return {"error": "Aucune information sur la batterie disponible"}
    except Exception as e:
        return {"error": str(e)}

# Fonction pour obtenir les informations sur les périphériques
def get_peripheral_info():
    try:
        if os.name == 'posix':
            peripherals = subprocess.check_output('lsusb', shell=True).decode()
        elif os.name == 'nt':
            peripherals = subprocess.check_output('wmic path Win32_USBControllerDevice get Dependent', shell=True).decode()
        else:
            peripherals = "OS non supporté pour cette fonctionnalité"
        return {"peripherals": peripherals}
    except Exception as e:
        return {"error": str(e)}

# Fonction pour obtenir les informations CPU
def get_cpu_info():
    return {
        "cpu_name": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "cpu_usage (%)": psutil.cpu_percent(interval=1)
    }

# Routes de l'API

## test
@app.route('/')
def principale():
    return "<p>azzedin za3Im</p>"

@app.route('/system_info', methods=['GET'])
def system_info():
    return jsonify(get_system_info())

@app.route('/memory_info', methods=['GET'])
def memory_info():
    return jsonify(get_memory_info())

@app.route('/battery_info', methods=['GET'])
def battery_info():
    return jsonify(get_battery_info())

@app.route('/peripheral_info', methods=['GET'])
def peripheral_info():
    return jsonify(get_peripheral_info())

@app.route('/cpu_info', methods=['GET'])
def cpu_info():
    return jsonify(get_cpu_info())

if __name__ == '__main__':
    app.run(debug=True)
