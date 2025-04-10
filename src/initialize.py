import threading
import time
import os
import datetime
import pyautogui

from src.helpers import helpers, logs
from src.macros import auto_item, detect_biome, detect_last_aura, auto_merchant, auto_potion_craft
from src.webhook import handle_webhook
from src.ui.popups import Popup


class Initialize:
    def __init__(self, ui):
        self.stop_macro_flag = False

        self.helpers = helpers.HelperFunctions()
        self.auto_item = auto_item.AutoItem(self)
        self.biome_detection = detect_biome.DetectBiome()
        self.craft_potions = auto_potion_craft.AutoPotion(self)
        self.auto_aura = detect_last_aura.DetectAura()
        self.merchant_handler = auto_merchant.AutoMerchant(self)
        self.webhook = handle_webhook.Webhook()

        self.ui = ui
        self.popup = Popup()

        self.data = self.helpers.load_config()
        self.images_path = os.path.join(os.getcwd(), "images")

        self.stopped = False
        self.set_variable_defaults()


    def set_variable_defaults(self):
        self.merchant_event = threading.Event()
        self.biome_randomizer_event = threading.Event()
        self.biome_detection_event = threading.Event()
        self.strange_controller_event = threading.Event()
        self.auto_potion_crafting_event = threading.Event()
        self.aura_clipping_event = threading.Event()

        self.lock = threading.Lock()

        self.stop_macro_flag = False

        self.last_merchant_teleporter_use = datetime.datetime.now()
        self.last_biome_randomizer_use = datetime.datetime.now()
        self.last_strange_controller_use = datetime.datetime.now()
        self.last_potion_swap = datetime.datetime.now()
        self.last_merchant_handled = None

        self.first_randomizer_use = True
        self.handling_merchant = False

        self.cur_last_aura = None
        self.current_biome = None

        self.biomes_list = [
            "NORMAL",
            "RAINY",
            "SNOWY",
            "WINDY",
            "HELL",
            "SAND STORM",
            "STARFALL",
            "CORRUPTION",
            "NULL",
            "DREAMSPACE",
            "GLITCHED"
        ]
        self.threads_locked = False
    

    def handle_error(self, error, error_func: str=None):
        logs.handle_log_msg('ERROR', error)
        self.end()

        self.popup.showerror(f"An error {error} has accured in the function {error_func}")


    def start(self):
        try:
            self.ui.after(0, lambda: self.ui.title("Nulled Sol's RNG Macro ( Starting )"))

            self.data = self.helpers.load_config()
            time.sleep(1)
            
            if self.helpers.link_checks():
                webhook_send = self.webhook.send_embed(title="**Macro Started!**", text="### Macro has been started")
                if webhook_send == 'ERROR':
                    self.end()

                    self.popup.showerror(message='Invalid Webhook URL')
                    return

            self.biome_detection_thread = threading.Thread(target=self.detect_biome, daemon=True)
            if self.data['detect_biome']['enabled'] == 1:
                self.biome_detection_event.clear()
                self.biome_detection_thread.start()

            self.aura_handling_thread = threading.Thread(target=self.clip_auras, daemon=True)
            if self.data['clip_aura']['enabled'] == 1:
                self.aura_clipping_event.clear()
                self.aura_handling_thread.start()

            self.merchant_thread = threading.Thread(target=self.auto_merchant, daemon=True)
            if self.data['auto_merchant']['enabled'] == 1:
                check_for_tesseract_ocr = self.helpers.check_for_tesseract()
                if check_for_tesseract_ocr == 'Not Found':
                    print('Tesseract not installed')

                self.merchant_event.clear()
                self.merchant_thread.start()

            self.auto_biome_randomizer_thread = threading.Thread(target=self.auto_biome_randomizer, daemon=True)
            if self.data['biome_randomizer']['enabled'] == 1:
                self.biome_randomizer_event.clear()
                self.auto_biome_randomizer_thread.start()
            
            self.auto_strange_controller_thread = threading.Thread(target=self.auto_strange_controller, daemon=True)
            if self.data['strange_controller']['enabled'] == 1:
                self.strange_controller_event.clear()
                self.auto_strange_controller_thread.start()
            
            self.auto_potion_crafting_thread = threading.Thread(target=self.auto_potion_crafting, daemon=True)
            if self.data['auto_potion']['enabled'] == 1:
                self.enabled_potions = []
                for potion in self.data['auto_potion']['potions']:
                    if self.data['auto_potion']['potions'][potion]['enabled'] == 1:
                        self.enabled_potions.append(potion)

                self.auto_potion_crafting_event.clear()
                self.auto_potion_crafting_thread.start()
            
            self.ui.after(0, lambda: self.ui.title("Nulled Sol's RNG Macro ( Started )"))
        
        except Exception as e:
            print(e)
            self.handle_error(e, 'start')


    def end(self):
        try:
            self.ui.after(0, lambda: self.ui.title("Nulled Sol's RNG Macro ( Stopping )"))
            self.stop_macro_flag = True

            self.merchant_event.set()
            self.biome_randomizer_event.set()
            self.biome_detection_event.set()
            self.auto_potion_crafting_event.set()
            self.aura_clipping_event.set()

            time.sleep(0.25)

            threads_to_close = [
                "merchant_thread", 
                "auto_biome_randomizer_thread",
                "auto_strange_controller_thread",
                "biome_detection_thread",
                "auto_potion_crafting_thread",
                "aura_handling_thread"
            ]

            for thread in threads_to_close:
                if hasattr(self, thread):
                    if getattr(self, thread).is_alive():
                        logs.handle_log_msg('INFO', f'Attempting to end thread {thread}')
                        getattr(self, thread).join()

                        logs.handle_log_msg('INFO', f'Ended thread {thread} successfully')

            self.set_variable_defaults()
            self.ui.after(0, lambda: self.ui.title("Nulled Sol's RNG Macro ( Stopped )"))

            if self.helpers.link_checks() and not self.stopped:
                self.webhook.send_embed(title="**Macro Stopped!**", text="### Macro has been stopped")
            
            self.stopped = True
        except Exception as e:
            self.handle_error(e, 'end')


    def auto_potion_crafting(self):
        try:
            self.cur_potion = self.enabled_potions[0]
        except IndexError:
            return

        self.auto_add_enabled = False
        self.swap_interval = self.data['auto_potion']['swap_interval']

        try:
            potion_index = 0
            while not self.auto_potion_crafting_event.is_set():
                with self.lock:
                    self.craft_potions.craft_potion(self.cur_potion, self.auto_add_enabled)
                    self.auto_add_enabled = True

                    if (datetime.datetime.now() - self.last_potion_swap).seconds >= self.swap_interval * 60 or self.cur_potion == 'godlike':
                        potion_index = (potion_index + 1) % len(self.enabled_potions)
                        self.cur_potion = self.enabled_potions[potion_index]

                        self.last_potion_swap = datetime.datetime.now()

                        if len(self.enabled_potions) <= 1:
                            pass
                        else:
                            self.auto_add_enabled = False
        
        except Exception as e:
            self.handle_error(e, 'auto_potion_crafting')

    
    def detect_biome(self):
        try:
            while not self.biome_detection_event.is_set():
                # with self.lock:
                    detected_biome = self.biome_detection.DetectBiome(self.biomes_list)
                    if detected_biome == self.current_biome or detected_biome == None:
                        pass

                    elif detected_biome != self.current_biome:
                        logs.handle_log_msg('INFO', f"Detect Biome Return: {detected_biome} | Last Detected Current Biome: {self.current_biome}")

                        if detected_biome in self.biomes_list:
                            self.current_biome = detected_biome

                            if self.current_biome == "GLITCHED":
                                if self.helpers.link_checks():
                                    self.webhook.send_embed(title="**Biome Detection**", 
                                        text=f"""
                                        # > **Biome Detected** - Glitched
                                        """, 
                                        color="0x0cab66",
                                        ping_type="everyone"
                                    )
                            elif self.current_biome == "DREAMSPACE":
                                if self.helpers.link_checks():
                                    self.webhook.send_embed(title="**Biome Detection**", 
                                        text=f"""
                                        # > **Biome Detected** - Dreamspace
                                        """, 
                                        color="0xf70fb9",
                                        ping_type="everyone"
                                    ) 

                            for biome in self.data['webhook']['normal_biomes_list']:
                                if biome in self.biomes_list and (self.data['webhook']['normal_biomes_list'][biome] == 1 and biome == self.current_biome):
                                    if self.helpers.link_checks():
                                        self.webhook.send_embed(title=f"**Biome Detection**", 
                                            text=f"""
                                            # > **Biome Detected** - {self.current_biome}
                                            """, 
                                            color="0x131313",
                                        ) 

                        if self.current_biome in ['GLITCHED', 'DREAMSPACE']:
                            if not self.threads_locked:
                                self.handling_merchant = False
                                self.lock_threads()
                        else:
                            if self.threads_locked:
                                self.unlock_threads()

                    time.sleep(0.1)

        except Exception as e:
            self.handle_error(e, 'detect_biome')
    

    def lock_threads(self):
        self.stop_macro_flag = True

        self.merchant_event.set()
        self.biome_randomizer_event.set()
        self.strange_controller_event.set()
        self.auto_potion_crafting_event.set()

    
    def unlock_threads(self):
        self.stop_macro_flag = False

        self.merchant_event.clear()
        self.biome_randomizer_event.clear()
        self.strange_controller_event.clear()
        self.auto_potion_crafting_event.clear()

    
    def clip_auras(self):
        try:
            while not self.aura_clipping_event.is_set():
                # with self.lock:
                    try:
                        last_equipped_aura = self.auto_aura.detect_aura()

                        time.sleep(0.1)
                        if last_equipped_aura == self.cur_last_aura or last_equipped_aura == None:
                            continue

                        elif last_equipped_aura != self.cur_last_aura:
                            logs.handle_log_msg('INFO', f"Detect Aura Return: {last_equipped_aura} | Last Cur Aura: {self.cur_last_aura}")

                            self.cur_last_aura = last_equipped_aura
                            rarity = self.helpers.get_aura_rarity(self.cur_last_aura)
                            
                            ping_type = None
                            try:
                                if rarity != "Aura Not Found":
                                    if rarity >= self.data['clip_aura']['min_clip_rarity']:
                                        hotkey = self.data['clip_aura']['clip_hotkey']
                                        keys = [key.strip() for key in hotkey.split('+')]

                                        for _ in range(100):
                                            time.sleep(0.1)
                                        pyautogui.hotkey(*keys)

                                    if rarity >= self.data['clip_aura']['min_ping_rarity']:
                                        ping_type = "aura_found"

                                    if rarity >= 1000:
                                        if self.helpers.link_checks():
                                            self.webhook.send_embed(title=f"**Aura Alert**", 
                                                text=f"""
                                                # > **Aura Found** | {self.cur_last_aura} | 1 / {rarity}
                                                """, 
                                                color="0x9d0202" if rarity >= 99999999 else "0x82bfff",
                                                ping_type=ping_type
                                            ) 
                                else:
                                    logs.handle_log_msg('INFO', f"Aura Rarity not found for aura {last_equipped_aura}")
                            except Exception as e:
                                self.handle_error(e, 'clip_auras')

                    except Exception as e:
                        self.handle_error(e, 'clip_auras')
                        for _ in range(50):
                            time.sleep(0.1)
        
        except Exception as e:
            self.handle_error(e, 'clip_auras')


    def auto_merchant(self):
        delay = self.data['auto_merchant']['interval']

        try:
            while not self.merchant_event.is_set() and self.current_biome not in ["GLITCHED", "DREAMSPACE"]:
                with self.lock:
                    if (datetime.datetime.now() - self.last_merchant_teleporter_use).seconds >= delay * 60:
                        if self.handling_merchant:
                            pass
                            
                        else:
                            self.auto_item.UseItem("Teleport", 1)
                            self.last_merchant_teleporter_use = datetime.datetime.now()

                            for _ in range(50):
                                time.sleep(0.1)

                            if self.last_merchant_handled is None or (datetime.datetime.now() - self.last_merchant_handled).seconds >= 180:
                                self.handle_buying_from_merchant()

                    time.sleep(0.1)
        
        except Exception as e:
            self.handle_error(e, 'auto_merchant')

    
    def handle_buying_from_merchant(self):
        try:
            self.handling_merchant = True

            check_for_tesseract_ocr = self.helpers.check_for_tesseract()
            if check_for_tesseract_ocr == True:
                handle_merchant = self.merchant_handler.handle_merchant()

                if handle_merchant in ['ERROR', 'No Merchant Found']:
                    self.handling_merchant = False
                    return
                
                self.last_merchant_handled = datetime.datetime.now()

            self.handling_merchant = False

        except Exception as e:
            self.handle_error(e, 'handle_buying_from_merchant')
            self.handling_merchant = False
    

    def auto_biome_randomizer(self):
        delay = self.data['biome_randomizer']['interval']
        
        try:
            while not self.biome_randomizer_event.is_set() and self.current_biome not in ["GLITCHED", "DREAMSPACE"] and not self.handling_merchant:
                with self.lock:
                    if (datetime.datetime.now() - self.last_biome_randomizer_use).seconds >= delay * 60 or self.first_randomizer_use == True:
                        print("Attempting to use biome randomizer")
                        self.auto_item.UseItem("Biome", 1)

                        self.last_biome_randomizer_use = datetime.datetime.now()
                        self.first_randomizer_use = False

                time.sleep(0.1)
        
        except Exception as e:
            self.handle_error(e, 'auto_biome_randomizer')

    
    def auto_strange_controller(self):
        delay = self.data['strange_controller']['interval']
        
        try:
            while not self.strange_controller_event.is_set() and self.current_biome not in ["GLITCHED", "DREAMSPACE"] and not self.handling_merchant:
                with self.lock:
                    if (datetime.datetime.now() - self.last_strange_controller_use).seconds >= delay * 60:
                        self.auto_item.UseItem("Controller", 1)

                        self.last_strange_controller_use = datetime.datetime.now()

                time.sleep(0.1)
        
        except Exception as e:
            self.handle_error(e, 'auto_strange_controller')

