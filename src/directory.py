import os, platform
import subprocess, logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# funcion que crea cualquier carpeta, en la ruta que se le pasa
def crearCarpeta(pathActual):
    try:
        if not os.path.exists(pathActual):
            os.makedirs(pathActual)
            logging.info(f"Carpeta creada: {pathActual}")
        return True
    except OSError as e:
        logging.error(f"No se pudo crear la carpeta {pathActual}: {e}")
        return False

# crear carpeta Fiesta
def crear_carpeta_fiesta():
    # obtener ruta raiz del usuario
    path_usr = os.path.expanduser("~")
    # por default la carpte se creara en el escritorio
    desk = "Desktop"
    nameDir = "Fiesta"
    # unir el nombre de la carpeta fiesta con el escritorio y con la ruta raiz
    path = os.path.join(path_usr,desk,nameDir)
    # crear carpeta fiesta
    crearCarpeta(path)

    return crear_subcarpetas_musica_karaoke(path)
# crear sub carpetas musica y karoke dentro de fiesta
def crear_subcarpetas_musica_karaoke(path):
    musica = "Musica"
    karaoke = "Karaoke"

    path_musica = os.path.join(path,musica)
    path_karoke = os.path.join(path,karaoke)

    crearCarpeta(path_musica)
    crearCarpeta(path_karoke)
    return path_musica,path_karoke

def abrirDir(tipo):
    m,k = crear_carpeta_fiesta()
    ruta = m if tipo == "audio" else k if tipo == "video" else None
    
    if ruta and os.path.exists(ruta):
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.Popen(['explorer', ruta])
            elif system == "Darwin":  # macOS
                subprocess.Popen(['open', ruta])
            else:  # Linux y otros
                subprocess.Popen(['xdg-open', ruta])
        except Exception as e:
            logging.error(f"No se pudo abrir la carpeta: {e}")
    else:
        logging.error(f"La ruta especificada no existe. Tipo: {tipo}")
