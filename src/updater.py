import requests, os, sys, subprocess
import webbrowser
from version import VERSION

def check_for_updates():
    url = "https://api.github.com/repos/DiegoMS0606/YT_Download/releases/latest"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        latest_version = data['tag_name'].replace("v", "")
        
        if latest_version != VERSION:
            asset = data['assets'][0]
            download_url = asset['browser_download_url']
            print(f"New version available: {latest_version}. You are using version: {VERSION}.")
            print("Opening the download page...")
            new_exe_path = os.path.join(os.path.dirname(sys.executable), "update_new.exe")
            
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(new_exe_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            print("Download completed. Launching the updater...")
            current_exe = sys.executable
            
            subprocess.Popen(["update_helper.bat", current_exe, new_exe_path])
            sys.exit(0)
        else:
            print("You are using the latest version.")
    except Exception as e:
        print(f'An exception occurred: {e}')