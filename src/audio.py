import yt_dlp as yt
import os, sys, logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_binary_path(binary_name):
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(bundle_dir, binary_name)
    
    if  not os.path.exists(ruta):
        logging.error(f"No se encontró el binario {binary_name} en la ruta {ruta}")
        
    return ruta


def descargaAudio(url, output_path,progress_hook):
    if progress_hook and not callable(progress_hook):
        raise ValueError("El progress_hook debe ser una función callable.")
    ffmpeg = get_binary_path('ffmpeg.exe')
    
    logging.info(f"Ruta de ffmpeg: {ffmpeg}")
    
    ydl_opts = {
        'outtmpl': output_path,
        'format':'bestaudio/best',
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality':'192',
        }],
        'progress_hooks': [progress_hook] if progress_hook else [],
        'ffmpeg_location': ffmpeg,
    }
    
    try:
        with yt.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logging.info("Descarga de audio completada.")
    except Exception as e:
        logging.error(f"Error al descargar el audio: {e}")