import os
import sys
import pathlib

import keyboard

sys.path.append(os.path.join(pathlib.Path(__file__).parent.resolve(), "src"))
sys.path.append(os.path.join(pathlib.Path(__file__).parent.resolve(), "src/helpers"))
sys.path.append(os.path.join(pathlib.Path(__file__).parent.resolve(), "src/macros"))
sys.path.append(os.path.join(pathlib.Path(__file__).parent.resolve(), "src/ui"))
sys.path.append(os.path.join(pathlib.Path(__file__).parent.resolve(), "src/webhook"))

from src.ui.gui import UI
from src.ui.popups import Popup
from src.helpers import logs, helpers
from src.initialize import Initialize


class Nulled:
    def __init__(self):
        self.start_flag = False
        self.end_flag = False

        self.ui = UI()
        self.init = Initialize(ui=self.ui)
        self.helper = helpers.HelperFunctions()
        self.popup = Popup()

        try:
            if self.checks() == True:
                keyboard.add_hotkey("F1", lambda: self.start_func())
                keyboard.add_hotkey("F2", lambda: self.end_func())

                self.ui.protocol("WM_DELETE_WINDOW", self.on_window_close)
                self.ui.mainloop()

            elif self.checks() == "Tesseract-OCR isn't installed":
                self.ui.after(0, lambda: self.popup.showinfo(message=f"Tesseract-OCR Not Found | Please install it to use auto merchant"))

            else:
                return
        
        except Exception as e:
            logs.handle_log_msg('ERROR', e)
            sys.exit(0)

    
    def checks(self):
        try:
            self.helper.update()

            if not os.path.exists("C:\\Program Files\\Tesseract-OCR\\tesseract.exe") or os.path.exists("C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"):
                return "Tesseract-OCR isn't installed"
            return True

        except Exception as e:
            logs.handle_log_msg('ERROR', e)
            print(e)
            return e


    def start_func(self):
        try:
            if not self.start_flag and not self.end_flag:
                self.start_flag = True

                self.data = self.helper.load_config()
                
                logs.handle_log_msg('INFO', f"{self.data['webhook_url']} | {self.data['private_server_link']}")
                if self.data['webhook_url'] == '':
                    self.ui.after(0, lambda: self.popup.showinfo(message="Webhook URL not added | Webhooks will NOT be sent"))

                with open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'error_log.log'), 'w') as f:
                    f.write('')

                self.init.start()
            self.start_flag = False
        
        except Exception as e:
            logs.handle_log_msg('ERROR', e)
            sys.exit(0)


    def end_func(self):
        try:
            if not self.end_flag:
                self.end_flag = True
                self.init.end()

            self.end_flag = False
            return
        
        except Exception as e:
            logs.handle_log_msg('ERROR', e)
            sys.exit(0)


    def on_window_close(self):
        self.end_func()
        sys.exit(0)


if __name__ == "__main__":

    nulled = Nulled()

