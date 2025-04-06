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
from src.helpers import logs, helpers
from initialize import Initialize


class Nulled:
    def __init__(self):
        self.start_flag = False
        self.end_flag = False

        self.init = Initialize()
        self.helper = helpers.HelperFunctions()
        self.ui = UI()

        try:
            if self.checks() == True:
                keyboard.add_hotkey("F1", lambda: self.start_func())
                keyboard.add_hotkey("F2", lambda: self.end_func())

                self.ui.protocol("WM_DELETE_WINDOW", self.on_window_close)
                self.ui.mainloop()

            elif self.checks() == "Tesseract-OCR isn't installed":
                print("Tesseract-OCR isn't installed, to use auto merchant you will need to install it")

            else:
                print("Required modules aren't installed")
        
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
                if self.data['webhook_url'] == '' or self.data['private_server_link'] == '':
                    logs.handle_log_msg('ERROR', f"{self.data['webhook_url']} | {self.data['private_server_link']}")
                    self.end_func()
                    
                    sys.exit(0)

                with open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'error_log.log'), 'w') as f:
                    f.write('')

                self.ui.after(0, lambda: self.ui.title("Nulled Sol's RNG Macro ( Started )"))
                self.init.start()
            self.start_flag = False
        
        except Exception as e:
            logs.handle_log_msg('ERROR', e)
            print(e)
            sys.exit(0)


    def end_func(self):
        try:
            if not self.end_flag:
                self.end_flag = True
                
                self.ui.after(0, lambda: self.ui.title("Nulled Sol's RNG Macro ( Stopping )"))
                self.init.end()

                self.ui.after(0, lambda: self.ui.title("Nulled Sol's RNG Macro ( Stopped )"))
            self.end_flag = False
            return
        
        except Exception as e:
            logs.handle_log_msg('ERROR', e)
            print(e)
            sys.exit(0)


    def on_window_close(self):
        self.end_func()
        sys.exit(0)


if __name__ == "__main__":
    nulled = Nulled()

