<h1 align="center">Merklemap 🐉</h1>

<p align="center">
  Herramienta de reconocimiento y mapeo de superficie de ataque mediante la API de Merklemap.
</p>

<p align="center">
  <img src="assets/Merklemap.png" title="Merklemap" alt="Merklemap" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python version">
  <img src="https://img.shields.io/badge/Docker-ready-blue?logo=docker&logoColor=white" alt="Docker Ready">
  <img src="https://img.shields.io/badge/License-MIT-green?logo=open-source-initiative&logoColor=white" alt="License">
</p>

---

## 🚀 Características

- Descubre subdominios asociados a un dominio principal
- Detecta tecnologías web utilizadas (Wappalyzer)
- Verifica certificados SSL y su fecha de expiración
- Identifica formularios de login y páginas de autenticación
- Captura pantallas automáticas de páginas interesantes
- Genera reportes en CSV y TXT con los resultados
- Interfaz intuitiva con visualización en tabla
- Banner de presentación con estilo único

## 📌 Requisitos

- Python 3.12+

- Librerías: `requests`, `colorama`, `beautifulsoup4`, `python-Wappalyzer`, `pyppeteer`, `chromedriver-autoinstaller`, `selenium`, `tabulate`, `urllib3`, `pyOpenSSL`

## 🔧 Requisitos adicionales

- **Chrome/Chromium**: Necesario para las capturas de pantalla

# En sistemas Debian/Ubuntu:
```bash
sudo apt install chromium
```

## ⚠️ Advertencia

#### Esta herramienta solo debe usarse para:

- Auditorías de seguridad autorizadas
- Pruebas de penetración con permiso
- Investigación de seguridad defensiva
- Propósitos educativos

###### No utilices esta herramienta para actividades ilegales o sin el consentimiento del propietario del dominio.

---
## ⚙️ Instalación

Clona el repositorio:

```bash
git clone https://github.com/HackUnderway/Merklemap.git
```
```bash
cd Merklemap
```
```bash
pip install -r requirements.txt
```

## 🐍 Uso básico en Python
##### Ejecuta el script:

python3 merklemap.py

##### Ingresa el dominio que deseas analizar (ejemplo: example.com)


## 🐳 Uso con Docker

Merklemap incluye un Dockerfile que configura automáticamente el contenedor con Python y todas las dependencias necesarias.
Esto te permite usar la herramienta **sin instalar nada en tu sistema host.**

###### 🏗️ Construir la imagen:
*Dentro del repositorio:*

```bash
sudo docker build -t merklemap .
```
```bash
sudo docker run -it --rm -v $(pwd)/resultados_merklemap:/app/resultados_merklemap merklemap
```

📌 **Nota:** Dentro del contenedor Docker ya viene:

- Python 3.12

- Todas las librerías necesarias (requests, selenium, etc.)

- Configuración lista para ejecutar merklemap.py

#### Así puedes elegir entre:
✔ Usarlo en Python directamente

✔ O ejecutar el contenedor Docker con todo preconfigurado

#### La herramienta:

1 - Consultará la API de Merklemap

2 - Filtrará los subdominios legítimos

3 - Analizará cada uno detectando tecnologías

4 - Verificará certificados SSL

5 - Capturará pantallas de páginas de login

6 - Generará reportes detallados


> **El proyecto está abierto a colaboradores.**

# DISTRIBUCIONES SOPORTADAS
|Distribución | Versión verificada | 	¿Soportado? | 	Estado |
|--------------|--------------------|------|-------|
|Kali Linux| 2025.2| si| funcionando   |
|Parrot Security OS| 6.3| si | funcionando   |
|Windows| 11 | si | funcionando   |
|BackBox| 9 | si | funcionando   |
|Arch Linux| 2024.12.01 | si | funcionando   |

# SOPORTE
Preguntas, errores o sugerencias: info@hackunderway.com

# LICENSE
- [x] Merklemap tiene licencia.
- [x] Consulta el archivo [LICENSE](https://github.com/HackUnderway/Merklemap#MIT-1-ov-file) para más información.

# CYBERSECURITY RESEARCHER

* [Victor Bancayan](https://www.offsec.com/bug-bounty-program/) - (**CEO at [Hack Underway](https://hackunderway.com/)**) 

## 🔗 ENLACES
[![Patreon](https://img.shields.io/badge/patreon-000000?style=for-the-badge&logo=Patreon&logoColor=white)](https://www.patreon.com/c/HackUnderway)
[![Web site](https://img.shields.io/badge/Website-FF7139?style=for-the-badge&logo=firefox&logoColor=white)](https://hackunderway.com)
[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/HackUnderway)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@JeyZetaOficial)
[![Twitter/X](https://img.shields.io/badge/Twitter/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/JeyZetaOficial)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/hackunderway)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-212C42?style=for-the-badge&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/JeyZeta)

## ☕️ Apoya el proyecto

Si te gusta esta herramienta, considera invitarme un café:

[![Buy Me a Coffee](https://img.shields.io/badge/-Buy%20me%20a%20coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/hackunderway)

## 🌞 Suscripciones

###### Suscríbete: [Jey Zeta](https://www.facebook.com/JeyZetaOficial/subscribe/)

[![Kali Linux](https://img.shields.io/badge/Kali_Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)](https://www.kali.org/)

from <img src="https://i.imgur.com/ngJCbSI.png" title="Perú"> made in <img src="https://i.imgur.com/NNfy2o6.png" title="Python"> with <img src="https://i.imgur.com/S86RzPA.png" title="Love"> by: <font color="red">Victor Bancayan</font>

© 2025
