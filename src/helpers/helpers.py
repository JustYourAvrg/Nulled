import json
import os
import sys
import pathlib
import autoit
import pytesseract
import requests
import webbrowser
import pygetwindow as gw

from helpers.logs import handle_log_msg
from ui.popups import showmsg, askyesno


class HelperFunctions:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)

        else:
            self.base_dir = pathlib.Path(__file__).parents[2].resolve()

        self.config_path = os.path.join(self.base_dir, 'config.json')
        self.aura_data_path = os.path.join(self.base_dir, 'aura_rarity.json')

        self.url = f"https://api.github.com/repos/JustYourAvrg/Nulled/releases/latest"

        self.config_data = self.load_config()


    def update(self):
        try:
            response = requests.get(self.url)

            if response.status_code == 200:
                latest_release = response.json()
                tag_name = latest_release.get('tag_name')

                if self.config_data['version'] != tag_name:
                    choice = self.popup.askyesno("Update", f"A New update has been detected {tag_name} would you like to update?")
                    if choice:
                        webbrowser.open(f"https://github.com/JustYourAvrg/Nulled/releases/tag/{tag_name}")
                        sys.exit(0)
                return

        except Exception as e:
            return e


    def check_for_tesseract(self):
        try:
            paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            ]

            for path in paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    return True
            
            return "Not Found"
        
        except Exception as e:
            handle_log_msg('ERROR', e)
            return "Not Found"


    def get_aura_rarity(self, aura: str):
        try:
            with open(self.aura_data_path, 'r') as f:
                aura_data = json.load(f)

            for item in aura_data:
                if item == aura:
                    return aura_data[item]["Rarity"]
            return "Aura Not Found"
        
        except Exception as e:
            handle_log_msg('ERROR', e)
            return "None"

    
    def get_roblox_log_file_data(self):
        try:
            roblox_log_files = os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox', 'logs')

            if os.path.exists(roblox_log_files):
                files = [os.path.join(roblox_log_files, f) for f in os.listdir(roblox_log_files) if f.endswith('.log')]
                latest_file = max(files, key=os.path.getmtime)

                return latest_file

            else:
                print("Roblox log file path can't be found")

        except Exception as e:
            handle_log_msg('ERROR', e)


    def log_file_data(self):
        try:
            log_file = self.get_roblox_log_file_data()
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.readlines()

        except Exception as e:
            handle_log_msg('ERROR', e)
            return []


    def activate_roblox_window(self):
        try:
            windows = gw.getAllTitles()
            roblox_window = None
            
            for window in windows:
                if "Roblox" in window:
                    roblox_window = gw.getWindowsWithTitle(window)[0]
                    break

            if roblox_window:
                try:
                    autoit.win_activate('Roblox')
                except Exception as e:
                    print(f"Failed to activate window: {e}")
            else:
                print("Roblox window not found.")
        
        except Exception as e:
            handle_log_msg('ERROR', e)
        
    
    def load_config(self):
        try:
            if self.check_config() == True:
                with open(self.config_path) as f:
                    data = json.load(f)

                return data
            return {}

        except Exception as e:
            handle_log_msg('ERROR', e)


    def edit_config(self, args: list[str], new_data):
        try:
            if self.check_config() == True:
                self.config_data = self.load_config()

                d = self.config_data
                for item in args[:-1]:
                    d = d.setdefault(item, {})
                
                d[args[-1]] = new_data
                with open(self.config_path, 'w') as f:
                    json.dump(self.config_data, f, indent=4)
                self.config_data = self.load_config()
        
        except Exception as e:
            handle_log_msg('ERROR', e)


    def check_config(self):
        try:
            if os.path.exists(self.config_path):
                return True
            return False

        except Exception as e:
            handle_log_msg('ERROR', e)
            return False
        

        