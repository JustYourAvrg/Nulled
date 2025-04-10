import autoit
import os
import pathlib
import time
import json
import datetime

from helpers.logs import handle_log_msg


class AutoPotion:
    def __init__(self, init_ref):
        self.config_path = os.path.join(pathlib.Path(__file__).parents[2].resolve(), 'config.json')
        with open(self.config_path, 'r') as f:
            self.data = json.load(f)

        self.init_ref = init_ref

        self.enabled_potions = []
        for potion in self.data['auto_potion']['potions']:
            if self.data['auto_potion']['potions'][potion]['enabled'] == 1:
                self.enabled_potions.append(potion)

        self.last_potion_swap = datetime.datetime.now()

        self.amount_keypresses = ['25', '{enter}']


    def craft_potion(self, potion, auto_add_bool):
        try:
            if potion in self.enabled_potions:
                handle_log_msg('INFO', f'Attempting to craft potion {potion}')

                for _ in range(20):
                    if self.init_ref.stop_macro_flag:
                        return
                    time.sleep(0.1)
                autoit.send('f')

                autoit.mouse_click('left', x=self.data['auto_potion']['positions']['search_bar'][0], y=self.data['auto_potion']['positions']['search_bar'][1])
                if 'godly' in potion:
                    autoit.send('Godly')
                else:
                    autoit.send(potion)

                if self.init_ref.stop_macro_flag:
                    return

                autoit.mouse_click('left', x=self.data['auto_potion']['positions'][potion][0], y=self.data['auto_potion']['positions'][potion][1])
                if not auto_add_bool:
                    autoit.mouse_click('left', x=self.data['auto_potion']['positions']['auto_button'][0], y=self.data['auto_potion']['positions']['auto_button'][1])

                if self.init_ref.stop_macro_flag:
                    return
                
                potion_positions_data = self.data['auto_potion']['potions'][potion]['positions']
                for pos in potion_positions_data:
                    if self.init_ref.stop_macro_flag:
                        return
                    
                    autoit.mouse_wheel('up', clicks=1)
                    time.sleep(0.1)

                    if 'amount' in pos:
                        autoit.mouse_click('left', x=potion_positions_data[pos][0], y=potion_positions_data[pos][1], clicks=3, speed=15)

                        for key in self.amount_keypresses:
                            if self.init_ref.stop_macro_flag:
                                return
                            
                            if key == '25' and 'celestial' in pos:
                                key = '2'
                                
                            autoit.send(key)
                            time.sleep(0.25)
                    
                    if self.init_ref.stop_macro_flag:
                        return
                    autoit.mouse_click('left', x=potion_positions_data[pos][0], y=potion_positions_data[pos][1])
                    time.sleep(0.1)

                if self.init_ref.stop_macro_flag:
                        return
                autoit.mouse_click('left', x=self.data['auto_potion']['positions']['craft_button'][0], y=self.data['auto_potion']['positions']['craft_button'][1])
                time.sleep(1)
    
        except Exception as e:
            handle_log_msg('ERROR', e)