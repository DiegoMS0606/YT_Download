import yt_dlp as yt
import logging, os, sys

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_binary_path(binary_name):
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        # Carpeta raíz del proyecto (una carpeta arriba de src)
        bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    ruta = os.path.join(bundle_dir, 'assets', 'ffmpeg', 'bin', binary_name)
    
    if not os.path.exists(ruta):
        logging.error(f"No se encontró el binario {binary_name} en la ruta {ruta}")
    return ruta

def descargaVideo(url, output_path, progress_hook=None):
    if not url or not url.strip():
        logging.error("La URL vacía, no se puede descargar.")
        return
    
    ffmpeg = get_binary_path('ffmpeg.exe')
    ffprobe = get_binary_path('ffprobe.exe')
    
    if not os.path.exists(ffmpeg):
        logging.error(f"No se encontró ffmpeg en {ffmpeg}")
        return
    
    if not os.path.exists(ffprobe):
        logging.error(f"No se encontró ffprobe en {ffprobe}")
        return
    

    carpeta = os.path.dirname(output_path)
    if not os.path.exists(carpeta):
        try:
            os.makedirs(carpeta, exist_ok=True)
            logging.info(f"Carpeta creada: {carpeta}")
        except Exception as e:
            logging.error(f"No se pudo crear la carpeta {carpeta}: {e}")
            return

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook] if progress_hook else [],
        'ignoreerrors': True,
        'ffmpeg_location': os.path.dirname(ffmpeg),
    }

    try:
        with yt.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            logging.info(f"Descarga completada: {output_path}")
    except yt.utils.DownloadError as e:
        logging.error(f"Error en la descarga: {e}")
    except Exception as e:
        logging.error(f"Ocurrió un error inesperado: {e}")
