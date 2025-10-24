import os
import subprocess
# funcion que crea cualquier carpeta, en la ruta que se le pasa
def crearCrapeta(pathActual):
    
    try:
        os.makedirs(pathActual,exist_ok = True)
        return True
    except OSError as e:
        return False

# crear carpeta Fiesta
def mkdir_Fiesta():
    # obtener ruta raiz del usuario
    path_usr = os.path.expanduser("~")
    # por default la carpte se creara en el escritorio
    desk = "Desktop"
    nameDir = "Fiesta"
    # unir el nombre de la carpeta fiesta con el escritorio y con la ruta raiz
    path = os.path.join(path_usr,desk,nameDir)
    # crear carpeta
    crearCrapeta(path)
    dirM,dirK = mkdirM_K(path)
    return dirM,dirK
# crear sub carpetas musica y karoke dentro de fiesta
def mkdirM_K(path):
    musica = "Musica"
    karaoke = "Karaoke"

    dirM = os.path.join(path,musica)
    dirK = os.path.join(path,karaoke)

    crearCrapeta(dirM)
    crearCrapeta(dirK)
    return dirM,dirK

def abrirDir(tipo):
    m,k=mkdir_Fiesta()
    a="audio"
    v="video"
    if tipo == a:
        subprocess.Popen(['explorer',m])
    elif tipo == v:
        subprocess.Popen(['explorer',k])
    else:
        print("Opcion no reconcida")
