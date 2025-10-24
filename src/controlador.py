import ventanaMain
import os
import re
from directory import mkdir_Fiesta
from video import descargaVideo
from audio import descargaAudio

TIPO_VIDEO = "video"
TIPO_AUDIO = "audio"


def descargarArchivo(tipo,url, progress_bar=None, update_message =None):
    if not url or not url.strip():
        if update_message:
            update_message("Error: La URL ingresada esta vacia")
            return
        
    url = url.strip()

    try:
        path_musica, path_karoke = mkdir_Fiesta()

        ruta_audio = os.path.join(path_musica, "%(title)s.%(ext)s")
        ruta_video = os.path.join(path_karoke, "%(title)s.%(ext)s")
        
        hook = _make_progress_hook(progress_bar, update_message)
        
        if tipo == TIPO_VIDEO:
            descargaVideo(url, ruta_video,hook)
        elif tipo == TIPO_AUDIO:
            descargaAudio(url, ruta_audio, hook)
        else:
            if update_message:
                update_message("Tipo de archivo no reconocido")

    except Exception as e:
        if update_message:
            update_message(f"Error al descargar el archivo: {e}")
            

def _make_progress_hook(progress_bar, update_message):
    def hook(d):
        if d['status'] == 'downloading':
            try:
                porcentaje = re.sub(r'[^\d.]', '', d['_percent_str'])
                progreso = float(porcentaje) / 100
                
                # Actualizar la barra de progreso
                if progress_bar:
                    progress_bar.set(progreso)
                    progress_bar.update_idletasks()
                    
            except ValueError as e:
                if update_message:
                    update_message(f"Error al procesar el porcentaje de descarga: {e}")
                
        
        elif d['status'] == 'finished':
            if progress_bar:
                progress_bar.set(1.0) 
            original_filename = os.path.basename(d['filename'])
            
            converted_filename = original_filename.replace('.webp', '.mp3').replace('.m4a', '.mp3')
            
            mensaje = f"Descarga completa: {converted_filename}" if os.path.exists(converted_filename) else f"Descarga completa: {original_filename}"
            
            if update_message:
                update_message(mensaje)
    return hook

