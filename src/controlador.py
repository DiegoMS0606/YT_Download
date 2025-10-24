import ventanaMain
import os
import re
from directory import mkdir_Fiesta
from video import descargaVideo
from audio import descargaAudio
def obtenerUrl():
    try:
        if ventanaMain.url:  # Asegúrate de que la variable global esté inicializada
            link = ventanaMain.url.get().strip()  # Usa strip() para eliminar espacios en blanco
            if link:
                return link
            else:
                print("Error: La URL ingresada está vacía.")
        else:
            print("Error: El campo de URL no está inicializado.")
    except Exception as e:
        print(f"Error al obtener la URL: {e}")
    return None

def descargarArchivo(tipo):
    url = obtenerUrl()

    if not url:
        print("No se pudo obtener una URL válida. Aborta la descarga.")
        return  # Termina la función si la URL no es válida

    try:
        m, k = mkdir_Fiesta()
        v = "video"
        a = "audio"
        d_pathM = os.path.join(m, "%(title)s.%(ext)s")
        d_pathK = os.path.join(k, "%(title)s.%(ext)s")
        
        if tipo == v:
            descargaVideo(url, d_pathK,progress_hook)
        elif tipo == a:
            descargaAudio(url, d_pathM, progress_hook)
        else:
            print("Tipo de archivo no reconocido")
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")

      
def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            # Eliminar caracteres no numéricos de la cadena usando expresiones regulares
            porcentaje = d['_percent_str']
            porcentaje_limpio = re.sub(r'[^\d.]', '', porcentaje)  # Mantener solo números y el punto decimal
            progreso = float(porcentaje_limpio) / 100  # Convertir a porcentaje entre 0 y 1
            
            # Actualizar la barra de progreso
            ventanaMain.progress_bar.set(progreso)
            ventanaMain.progress_bar.update_idletasks()  # Forzar la actualización de la UI
            
        except ValueError as e:
            print(f"Error al procesar el porcentaje de descarga: {e}")
    
    if d['status'] == 'finished':
        ventanaMain.progress_bar.set(1.0)  # Asegúrate de que la barra se complete al final
        original_filename = os.path.basename(d['filename'])  # Obtén el nombre del archivo descargado
        
        # Si hay un post-procesado (como convertir a MP3), el archivo final debe ser el resultado
        # Puedes verificar si el archivo fue convertido a MP3 usando 'postprocessors'
        converted_filename = original_filename.replace('.webp', '.mp3').replace('.m4a', '.mp3')
        
        # Verifica si el archivo MP3 ya existe después de la conversión
        if os.path.exists(converted_filename):
            ventanaMain.updateMessage(f"Descarga completa: {converted_filename}")
        else:
            ventanaMain.updateMessage(f"Descarga completa: {original_filename}")