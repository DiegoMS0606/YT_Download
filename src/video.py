import yt_dlp as yt 

def descargaVideo(url, output_path,progress_hook):
    
    
    ydl_opts = {
        'outtmpl': output_path,
        'format':'best',
        'progress_hooks': [progress_hook],
        'postprocessor_args': ['--no-color'],
        
    }
    
    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])