import os,re
import yt_dlp as yt
from directory import crear_carpeta_fiesta as mkdir_Fiesta
from video import descargaVideo
from audio import descargaAudio
import threading

TIPO_VIDEO = "video"
TIPO_AUDIO = "audio"


def descargarArchivo(tipo,url, progress_bar=None, update_message =None):
    def tarea():
        if not url or not url.strip():
            if update_message:
                update_message("Error: La URL ingresada está vacía")
            return

        url_limpia = url.strip()

        try:
            path_musica, path_karoke = mkdir_Fiesta()

            ruta_audio = os.path.join(path_musica, "%(title)s.%(ext)s")
            ruta_video = os.path.join(path_karoke, "%(title)s.%(ext)s")
            
            titulo = sanitize_filename(yt_info_titulo(url_limpia))

            if tipo == TIPO_VIDEO:
                final_file = os.path.join(path_karoke, f"{titulo}.mp4")
            elif tipo == TIPO_AUDIO:
                final_file = os.path.join(path_musica, f"{titulo}.mp3")
            else:
                if update_message:
                    update_message("Tipo de archivo no reconocido")
                return

            # Verificar si el archivo ya existe
            if os.path.exists(final_file):
                if progress_bar:
                    progress_bar.set(1.0)
                    progress_bar.progress_color = "#FFD230"
                    progress_bar.update_idletasks()
                if update_message:
                    update_message(f"El archivo ya existe: {os.path.basename(final_file)}")
                return

            # Luego crear el hook y descargar
            hook = _make_progress_hook(progress_bar, update_message)

            if tipo == TIPO_VIDEO:
                descargaVideo(url_limpia, os.path.join(path_karoke, "%(title)s.%(ext)s"), hook)
            elif tipo == TIPO_AUDIO:
                descargaAudio(url_limpia, os.path.join(path_musica, "%(title)s.%(ext)s"), hook)

            if progress_bar:
                progress_bar.set(1.0)
            if update_message:
                update_message(f"Descarga completa: {os.path.basename(final_file)}")

        except Exception as e:
            if update_message:
                update_message(f"Error al descargar el archivo: {e}")

    
    hilo = threading.Thread(target=tarea)
    hilo.start()
            

def _make_progress_hook(progress_bar, update_message):
    tamanio_mayor = {'valor': 0}  # Guarda el tamaño del stream más grande

    def hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)

            # Ignorar descargas parciales de menor tamaño (audio, fragmentos)
            if total_bytes and total_bytes > tamanio_mayor['valor']:
                tamanio_mayor['valor'] = total_bytes

            # Mostrar progreso solo del stream más grande
            if total_bytes == tamanio_mayor['valor']:
                progreso = downloaded_bytes / total_bytes
                if progress_bar:
                    progress_bar.set(progreso)
                    progress_bar.update_idletasks()
                if update_message:
                    update_message(f"Descargando: {progreso*100:.1f}%")

        elif d['status'] == 'finished':
            # Esta parte ocurre cuando cada stream termina (antes del merge)
            if progress_bar:
                progress_bar.set(1.0)
            if update_message:
                update_message("Procesando archivo final...")

    return hook

def yt_info_titulo(url):
    with yt.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'archivo')
    
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)