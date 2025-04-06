import autoit
import time

from helpers.helpers import HelperFunctions
from helpers import logs


class AutoItem:
    def __init__(self, init_ref):
        self.helper = HelperFunctions()
        self.data = self.helper.load_config()

        self.init_ref = init_ref
        

    def UseItem(self, item_name, amount):
        search_bar_text = str(item_name)
        amount_list = [f"{amount}", "{enter}"]

        try:
            for position in self.data['inventory_mouse_positions']:
                autoit.mouse_click("left", self.data['inventory_mouse_positions'][position][0], self.data['inventory_mouse_positions'][position][1], 1, 5)
                if self.init_ref.stop_macro_flag:
                    return
                
                if position == "amount":
                    autoit.mouse_click('left', clicks=3, speed=5)
                    if self.init_ref.stop_macro_flag:
                        return

                    for key in amount_list:
                        if self.init_ref.stop_macro_flag:
                            return
                    
                        autoit.send(key)
                        time.sleep(0.2)
                elif position == "search_bar":
                    if self.init_ref.stop_macro_flag:
                        return
                    
                    autoit.send(search_bar_text)
                    time.sleep(0.1)
        
        except Exception as e:
            logs.handle_log_msg('ERROR', e)
            return