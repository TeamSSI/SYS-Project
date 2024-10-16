#!/usr/bin/python3

import platform
import psutil
import os
import subprocess
import pyfiglet # pour le banner
import socket # ceci cest pour fair la  connexion avec les machines a distance
from colorama import init,Fore,Style #pour le donner un designe aux banner



#la fonction utliser pour creer le banner
def create_banner(text , color=Fore.WHITE):
	banner=pyfiglet.figlet_format(text,font="slant")
	print(f"{color}{banner}{Style.RESET_ALL}")

#la fonction pour donner les information de system

def get_system_info():
	print("\n--- Informations sur le Système ---")
	print(f"Système d'exploitation : {platform.system()} {platform.release()} ({platform.version()})") #cela vas donner le nom de  OS + la version  par exe windows 10 
	print(f"Processeur : {platform.processor()}") #cela vas donner le nom de processeur
	print(f"Architecture : {platform.architecture()[0]}") #cela vas donner est ce que la machine est 64bit ou 32bit


#la fonction pour donner les inforamtions de memoire
def get_memory_info():
	print("\n--- Informations sur la Mémoire ---")
	memory = psutil.virtual_memory()
	print(f"Taille totale de la mémoire : {memory.total / (1024 ** 3):.2f} GB")
	print(f"Mémoire disponible : {memory.available / (1024 ** 3):.2f} GB")
	print(f"Utilisation de la mémoire : {memory.percent}%")


#la fonction pour donner les inforamtions  de perepherique
def get_peripheral_info():
	print("\n--- Informations sur les Périphériques ---")
	try:
		# Lister les périphériques connectés (Unix/Linux/Mac)
		if os.name == 'posix':
			peripherals = subprocess.check_output('lsusb', shell=True).decode()
			print(f"Périphériques USB :\n{peripherals}")
		# Afficher les périphériques pour Windows
		elif os.name == 'nt':
			peripherals = subprocess.check_output('wmic path Win32_USBControllerDevice get Dependent', shell=True).decode()
			print(f"Périphériques USB :\n{peripherals}")
	except Exception as e:
		print(f"Erreur lors de la récupération des périphériques : {e}")

#la fonction utiliser pour donner les informations sur la battrie
def get_battery_info():
    print("\n--- Informations sur la Batterie ---")
    try:
        # Vérification pour les systèmes Linux
        if os.name == 'posix':
            battery = psutil.sensors_battery()
            if battery:
                print(f"Niveau de la batterie : {battery.percent}%")
                print(f"Branché : {'Oui' if battery.power_plugged else 'Non'}")
                path = "/sys/class/power_supply/BAT1/"
                try:
                    energy_now = int(open(os.path.join(path, "energy_now")).read())
                    power_now = int(open(os.path.join(path, "power_now")).read())
                    if power_now > 0:
                        time_left = energy_now / power_now * 60  # convert to minutes
                        print(f"Temps restant : {time_left:.2f} minutes")
                    else:
                        print("Impossible de calculer le temps restant.")
                except FileNotFoundError:
                    print("Impossible de trouver les fichiers d'information sur la batterie.")
            else:
                print("Aucune information sur la batterie disponible (pas un laptop ou capteur non détecté).")

        # Vérification pour Windows
        elif os.name == 'nt':
            battery = psutil.sensors_battery()
            if battery:
                print(f"Niveau de la batterie : {battery.percent}%")
                print(f"Branché : {'Oui' if battery.power_plugged else 'Non'}")
                print(f"Temps restant : {battery.secsleft // 60} minutes" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Temps restant : Inconnu")
            else:
                print("Aucune information sur la batterie disponible (pas un laptop ou capteur non détecté).")

    except Exception as e:
        print(f"Erreur lors de la récupération des informations de la batterie : {e}")




def get_cpu_info():
        print("\n--- Informations sur le CPU ---")
        print(f"Nom de la CPU : {platform.processor()}")
        print(f"Nombre de cœurs : {psutil.cpu_count(logical=False)}")
        print(f"Nombre de threads (cœurs logiques) : {psutil.cpu_count(logical=True)}")
        print(f"Utilisation de la CPU : {psutil.cpu_percent(interval=1)}%")


def local_recon():
	print("\n--- Reconnaissance Locale ---")
	# le nom de ma machine + l'address ip cest facultative
	print(f"Nom de la machine : {socket.gethostname()}")
	print(f"Adresse IP : {socket.gethostbyname(socket.gethostname())}")
	#l'appelle des fonction
	get_cpu_info()
	get_memory_info()
	get_system_info()
	get_peripheral_info()
	get_battery_info()

if __name__=="__main__":

	create_banner("RECON" , color=Fore.CYAN)

while True:
	print("\n Choisissez une option :")
	print("1. Reconnaissance Local")
	print("2. Reconnaissance a Distance")
	print("3. Quitter")

	choix=input("Votre choix est (1/2/3) : ").strip()

	if choix== '1':
		local_recon()
	elif choix == '2':
		print("mazal")
	elif choix == '3':
		print("by by!!")
		break
	else:
		print("choix invalide , veuillez entrer 1 ou 2 ou 3")


