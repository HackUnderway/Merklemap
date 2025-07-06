import requests
import os
import csv
import time
import threading
import itertools
import warnings
from datetime import datetime
from colorama import init, Fore, Style
from tabulate import tabulate
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urlparse
from Wappalyzer import Wappalyzer, WebPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ssl
import OpenSSL

os.system("printf '\033]2;Merklemap v1.0 🐉\a'")

# Configuración inicial
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Banner degradado ---
def colorize_truecolor(text, bold=True):
    """
    Aplica un degradado verde (oscuro -> claro) usando colores TrueColor (24 bits)
    """
    lines = text.split("\n")
    total_lines = len(lines)
    colored_lines = []

    for i, line in enumerate(lines):
        green = int(50 + (i / max(total_lines - 1, 1)) * (255 - 50))
        r, g, b = 0, green, 0  # Verde puro
        bold_code = "\033[1m" if bold else ""
        color_code = f"{bold_code}\033[38;2;{r};{g};{b}m"
        colored_lines.append(f"{color_code}{line}\033[0m")

    return "\n".join(colored_lines)

dragon_banner = """
            ..,;:ccc,.
          ......''';lxO.
.....''''..........,:ld;
           .';;;:::;,,.x,
      ..'''.            0Xxoc:,.  ...
  ....                ,ONkc;,;cokOdc',.
 .                   OMo           ':ddo.
                    dMc               :OO;
                    0M.                 .:o.
                    ;Wd
                     ;XO,
                       ,d0Odlc;,..
                           ..',;:cdOOd::,.
                                    .:d;.':;.
                                       'd,  .'
                                         ;l   ..
                                          .o
                                            c
                                            .'
                                             .
"""

def mostrar_banner():
    print(colorize_truecolor(dragon_banner))
    print(f"{Fore.GREEN}[ Recon & Attack Surface Mapper ]{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}By: Hack Underway{Style.RESET_ALL}\n")

# --- Funciones auxiliares ---
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def crear_carpeta_si_no_existe(nombre_carpeta):
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)

def mostrar_loader(mensaje, detener_evento):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if detener_evento.is_set():
            break
        print(f"\r⏳ {mensaje}... {c}", end='', flush=True)
        time.sleep(0.1)

def es_subdominio_legitimo(hostname, dominio_principal):
    return hostname.endswith(f".{dominio_principal}") or hostname == dominio_principal

# --- Funciones de análisis ---
def detectar_tecnologias(url):
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module="Wappalyzer")
            wappalyzer = Wappalyzer.latest()
            webpage = WebPage.new_from_url(url, verify=False)
            tecnologias = wappalyzer.analyze(webpage)
            return ", ".join(tecnologias) if tecnologias else "No detectado"
    except Exception as e:
        return f"Error: {str(e)}"

def capturar_pantalla(url, nombre_archivo):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,1024")
        options.add_argument('--log-level=3')
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        driver.save_screenshot(nombre_archivo)
        driver.quit()
        return True
    except Exception as e:
        print(f"\n⚠️ Error al capturar {url}: {str(e)}")
        return False

def verificar_certificado(hostname):
    try:
        cert = ssl.get_server_certificate((hostname, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        expiracion = x509.get_notAfter().decode('utf-8')
        fecha_exp = datetime.strptime(expiracion, '%Y%m%d%H%M%SZ')
        dias_restantes = (fecha_exp - datetime.now()).days
        emisor = x509.get_issuer().CN
        return f"Válido ({dias_restantes}d) | Emisor: {emisor}"
    except Exception as e:
        return f"Error: {str(e)}"

def verificar_url(hostname, capturas_dir):
    url = f"https://{hostname}"
    try:
        session = requests.Session()
        response = session.get(url, timeout=3, verify=False, allow_redirects=True)
        final_url = response.url.lower()
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            has_input = bool(soup.find('input'))
            tecnologias = detectar_tecnologias(url)
            
            screenshot_path = None
            login_keywords = ["login", "logon", "auth", "signin", "acceso"]
            if any(keyword in final_url for keyword in login_keywords) or has_input:
                screenshot_path = os.path.join(capturas_dir, f"{hostname.replace('/', '_')}.png")
                capturar_pantalla(url, screenshot_path)
            
            estado = "Funcional"
            if any(keyword in final_url for keyword in login_keywords):
                estado = f"Redirige a login ({final_url})"
            elif has_input:
                estado = "Formulario detectado"
            
            return {
                "hostname": hostname,
                "estado": estado,
                "tecnologias": tecnologias,
                "certificado": verificar_certificado(hostname),
                "screenshot": screenshot_path
            }
        return None
    except Exception as e:
        return None

# --- Función principal ---
def main():
    limpiar_consola()
    mostrar_banner()

    dominio = input("Ingresa la URL que quieres buscar (ej. hackerone.com): ").strip().lower()
    dominio = dominio.replace("https://", "").replace("http://", "").split("/")[0]  # Limpieza
    
    crear_carpeta_si_no_existe("resultados_merklemap")
    capturas_dir = os.path.join("resultados_merklemap", "capturas")
    crear_carpeta_si_no_existe(capturas_dir)
    
    print("\n🎯 Iniciando análisis...\n")

    detener_evento = threading.Event()
    loader_thread = threading.Thread(target=mostrar_loader, args=("Escaneando dominios", detener_evento))
    loader_thread.start()

    inicio = time.time()

    try:
        response = requests.get(
            f"https://api.merklemap.com/v1-webui/search-noauth?query=.{dominio}&page=0",
            timeout=10
        )
        data = response.json()
    except Exception as e:
        detener_evento.set()
        loader_thread.join()
        print(f"\n❌ Error al conectar con Merklemap: {str(e)}")
        return

    resultados = []
    for item in data.get("results", []):
        hostname = item.get("hostname", "").lower()
        if not es_subdominio_legitimo(hostname, dominio):
            continue
            
        resultado = verificar_url(hostname, capturas_dir)
        if resultado:
            resultados.append([
                hostname,
                item.get("subject_common_name", ""),
                item.get("first_seen", ""),
                resultado["estado"],
                resultado["tecnologias"],
                resultado["certificado"],
                resultado["screenshot"] or "N/A"
            ])

    detener_evento.set()
    loader_thread.join()
    duracion = round(time.time() - inicio, 2)

    print(f"\n⏱ Análisis completado en {duracion} segundos")
    print(f"🔍 Dominio analizado: {dominio}")
    print(f"📌 Sitios funcionales encontrados: {len(resultados)}\n")

    if resultados:
        headers = ["Hostname", "Common Name", "Primera vista", "Estado", "Tecnologías", "Certificado SSL", "Captura"]
        
        tabla_consola = []
        for r in resultados:
            color = Fore.GREEN if "login" in r[3].lower() else Fore.YELLOW
            tabla_consola.append([
                r[0],
                r[1],
                r[2],
                f"{color}{r[3]}{Style.RESET_ALL}",
                r[4][:30] + "..." if len(r[4]) > 30 else r[4],
                r[5].split("|")[0]
            ])

        print(tabulate(tabla_consola, headers=headers[:-1], tablefmt="grid"))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = os.path.join("resultados_merklemap", f"{dominio}_{timestamp}.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f_csv:
            writer = csv.writer(f_csv)
            writer.writerow(headers)
            writer.writerows(resultados)
        
        txt_path = os.path.join("resultados_merklemap", f"{dominio}_{timestamp}.txt")
        with open(txt_path, "w", encoding="utf-8") as f_txt:
            f_txt.write(f"⏱ Análisis completado en {duracion} segundos\n")
            f_txt.write(f"🔍 Dominio analizado: {dominio}\n")
            f_txt.write(f"📌 Sitios funcionales encontrados: {len(resultados)}\n\n")
            
            headers_txt = headers[:-1]
            tabla_txt = []
            for r in resultados:
                tabla_txt.append([r[0], r[1], r[2], r[3], r[4], r[5].split("|")[0]])
            
            f_txt.write(tabulate(tabla_txt, headers=headers_txt, tablefmt="grid"))
            f_txt.write("\n\n💾 Capturas disponibles en: " + capturas_dir)

        print(f"\n💾 Resultados guardados en:")
        print(f"- 📄 CSV completo: {csv_path}")
        print(f"- 📝 TXT formateado: {txt_path}")
        print(f"- 🖼️ Capturas en: {capturas_dir}/")
    else:
        print("⚠️ No se encontraron subdominios funcionales.")

if __name__ == "__main__":
    main()
