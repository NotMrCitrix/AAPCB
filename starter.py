import ctypes
import os
import sys
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# Constants and file paths
AAPCB_DIR = os.path.join(os.getenv('PROGRAMFILES'), 'AAPCB')
STARTUP_FOLDER = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
CONFIG_FILE = 'config.txt'
UPDATE_SCRIPT = 'UpdateHosts.ps1'
RUN_UPDATER_BAT = 'run updater.bat'

URLS = {
    'run_updater_bat': 'https://raw.githubusercontent.com/NotMrCitrix/AAPCB/main/run%20updater.bat',
    'update_script': 'https://raw.githubusercontent.com/NotMrCitrix/AAPCB/main/UpdateHosts.ps1',
    'config_file': 'https://raw.githubusercontent.com/NotMrCitrix/AAPCB/main/config.txt'
}

def download_file(url, dest):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(dest, 'wb') as file:
            file.write(response.content)
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")

def setup_application(interval):
    # Ensure AAPCB directory exists
    if not os.path.exists(AAPCB_DIR):
        os.makedirs(AAPCB_DIR)

    # Check and download run updater.bat if not exists
    bat_file_path = os.path.join(STARTUP_FOLDER, RUN_UPDATER_BAT)
    if not os.path.exists(bat_file_path):
        download_file(URLS['run_updater_bat'], bat_file_path)

    # Check and download UpdateHosts.ps1 if not exists
    update_script_path = os.path.join(AAPCB_DIR, UPDATE_SCRIPT)
    if not os.path.exists(update_script_path):
        download_file(URLS['update_script'], update_script_path)

    # Check and download config.txt if not exists
    config_file_path = os.path.join(AAPCB_DIR, CONFIG_FILE)
    if not os.path.exists(config_file_path):
        download_file(URLS['config_file'], config_file_path)

    # Update the config.txt with the interval from the entry field
    if interval.isdigit():
        interval = int(interval)
        with open(config_file_path, 'r') as file:
            config_data = file.readlines()
        with open(config_file_path, 'w') as file:
            for line in config_data:
                if line.startswith("interval="):
                    file.write(f"interval={interval}\n")
                else:
                    file.write(line)
        update_status(f"Setup complete! Files have been set up.")
    else:
        update_status("Please enter a valid number for the update interval.")

def run_as_admin(script_path):
    shell32 = ctypes.windll.shell32
    shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)

def update_status(message):
    status_label.config(text=f"Status: {message}")

def on_download_app():
    interval = entry_update_interval.get()
    setup_application(interval)

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Setup Application")
    root.geometry("400x250")
    root.configure(bg='#333333')  # Dark background

    # Title Label
    title_label = tk.Label(root, text="Setup Application", fg="white", bg="#333333", font=("Arial", 16))
    title_label.pack(pady=10)

    # Update Interval Entry
    tk.Label(root, text="Update Interval (minutes):", fg="white", bg="#333333").pack(pady=5)
    global entry_update_interval
    entry_update_interval = tk.Entry(root, bg="white", fg="black", bd=0, relief='flat')
    entry_update_interval.pack(pady=5, padx=20, fill='x')

    # Download App Button
    download_button = tk.Button(root, text="Download App", command=on_download_app, bg="#007BFF", fg="white", font=("Arial", 12),
                               relief='flat', padx=10, pady=5)
    download_button.pack(pady=20, padx=20, fill='x')

    # Status Label
    global status_label
    status_label = tk.Label(root, text="Status: Waiting", fg="white", bg="#333333")
    status_label.pack(pady=10)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            main()
        else:
            script_path = os.path.abspath(__file__)
            run_as_admin(script_path)
    except Exception as e:
        print(f"Failed to check for admin rights: {e}")
