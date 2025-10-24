import yt_dlp as yt 

import logging, os

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def descargaVideo(url, output_path,progress_hook=None, ffmpeg_path=None):
    if not url or not url.strip():
        logging.error("La URL vacía, no se puede descargar.")
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
        'format': 'best',
        'progress_hooks': [progress_hook] if progress_hook else [],
        'postprocessor_args': ['--no-color'],
        'ignoreerrors': True,  # continuar si hay errores en algunos videos
    }
    
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path

    try:
        with yt.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            logging.info(f"Descarga completada: {output_path}")
    except yt.utils.DownloadError as e:
        logging.error(f"Error en la descarga: {e}")
    except Exception as e:
        logging.error(f"Ocurrió un error inesperado: {e}")