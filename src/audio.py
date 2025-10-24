import yt_dlp as yt
import os, sys

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        # Carpeta del ejecutable
        bundle_dir = sys._MEIPASS
        print(f"1: {bundle_dir}")
    else:
        # Carpeta del script de Python
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"2: {bundle_dir}")
    # Ruta relativa a la carpeta ffmpeg dentro del proyecto
    return os.path.join(bundle_dir,'ffmpeg.exe')

def get_ffprobe_path():
    
    # Similar al ffmpeg, obtener la ruta relativa de ffprobe
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        print(f"3: {bundle_dir}")
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"4: {bundle_dir}")
    
    return os.path.join(bundle_dir,'ffprobe.exe')

def descargaAudio(url, output_path,progress_hook):
    ffmpeg = get_ffmpeg_path()
    ffprobe = get_ffprobe_path()
    print(f"ffmpeg: {ffmpeg}")
    print(f"ffprobe: {ffprobe}")
    
    ydl_opts = {
        'outtmpl': output_path,
        'format':'bestaudio/best',
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality':'192',
        }],
        'progress_hooks': [progress_hook],
        'ffmpeg_location': ffmpeg,
        
        'ffprobe_location': ffprobe,
    }
    
    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])