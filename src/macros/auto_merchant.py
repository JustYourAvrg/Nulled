import autoit
import pyautogui
import time
import pathlib
import os
import pytesseract


from fuzzywuzzy import fuzz
from helpers.helpers import HelperFunctions
from helpers.logs import handle_log_msg
from src.webhook.handle_webhook import Webhook


class AutoMerchant:
    def __init__(self, init_ref):
        self.helper = HelperFunctions()
        self.webhook = Webhook()

        self.init_ref = init_ref
        
        self.images_path = os.path.join(pathlib.Path(__file__).parents[2].resolve(), 'images')
    

    def handle_dialogue(self, time_var):
        autoit.mouse_move(self.merchant_positions['dialogue box'][0], self.merchant_positions['dialogue box'][1])

        autoit.mouse_down('left')
        for _ in range(time_var * 10):
            if self.init_ref.stop_macro_flag:
                return
            time.sleep(0.1)

        autoit.mouse_up('left')


    def handle_ocr_miss(self, text):
        mari_items = [item for item in self.data['auto_merchant']['mari']]
        jester_items = [item for item in self.data['auto_merchant']['jester']]

        key = [*mari_items, *jester_items, 'mari', 'jester']

        try:
            cleaned_text = "".join(filter(str.isalpha, text)).strip()
            best_match = None
            best_similarity = 0

            for name in key:
                name.strip().lower()

                similarity = fuzz.ratio(cleaned_text.lower(), name)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = name

            handle_log_msg("DEBUG", f"BEST MATCH: {best_match} | BEST_SIMILARITY: {best_similarity} Python log line 54")
            return best_match if best_similarity > 60 else cleaned_text

        except Exception as e:
            handle_log_msg("ERROR", e, 'Python log line 58')
            return "ERROR"


    def handle_merchant(self):
        self.data = self.helper.load_config()

        self.merchant_positions = self.data['auto_merchant']['merchant_positions']

        autoit.send('e')
        for _ in range(20):
            if self.init_ref.stop_macro_flag:
                return
            time.sleep(0.1)

        if self.init_ref.stop_macro_flag:
            return
        self.handle_dialogue(3)
        
        if self.init_ref.stop_macro_flag:
            return
        try:
            merchant_name_screenshot = pyautogui.screenshot(region=[
                self.data['auto_merchant']['merchant_positions']['merchant name pos'][0],
                self.data['auto_merchant']['merchant_positions']['merchant name pos'][1],
                self.data['auto_merchant']['merchant_positions']['merchant name pos'][2],
                self.data['auto_merchant']['merchant_positions']['merchant name pos'][3]
            ])
            merchant_name_screenshot.save(f"{self.images_path}\\merchant.png")
            merchant_name = pytesseract.image_to_string(merchant_name_screenshot)
            merchant_name = str(merchant_name).lower()

            checked_merchant_name = self.handle_ocr_miss(merchant_name)
            handle_log_msg("INFO", f"MERCHANT NAME: {checked_merchant_name} Python log line 99")

            if str(checked_merchant_name).lower() in ['mari', 'jester']:
                self.items_to_buy = []

                if checked_merchant_name == 'mari':
                    for item in self.data['auto_merchant']['mari']:
                        if self.data['auto_merchant']['mari'][item]['enabled'] == 1:
                            self.items_to_buy.append(item.strip().lower())
                elif checked_merchant_name == 'jester':
                    for item in self.data['auto_merchant']['jester']:
                        if self.data['auto_merchant']['jester'][item]['enabled'] == 1:
                            self.items_to_buy.append(item.strip().lower())

                if self.init_ref.stop_macro_flag:
                    return
                handle_log_msg("DEBUG", f"{self.items_to_buy} Python log line 117")

                autoit.mouse_click('left', x=self.merchant_positions['open button'][0], y=self.merchant_positions['open button'][1])
                for _ in range(10):
                    if self.init_ref.stop_macro_flag:
                        return
                first_item_pos_x = self.merchant_positions['first item pos'][0]

                autoit.mouse_click('left', x=first_item_pos_x, y=self.merchant_positions['first item pos'][1])
                time.sleep(0.25)

                if self.helper.link_checks():
                    self.webhook.send_embed(title=f"**Merchant Alert**",
                        text=f"""
                        # > **{checked_merchant_name.capitalize()} Found**
                        """,
                    )

                for _ in range(5):
                    if self.init_ref.stop_macro_flag:
                        return
                    handle_log_msg("DEBUG", f"Checking item at position {first_item_pos_x} Python log line 132")

                    autoit.mouse_click('left', x=first_item_pos_x, y=self.merchant_positions['first item pos'][1])
                    time.sleep(2.5)

                    merchant_item_screenshot = pyautogui.screenshot(region=[
                        self.data['auto_merchant']['merchant_positions']['item name pos'][0],
                        self.data['auto_merchant']['merchant_positions']['item name pos'][1],
                        self.data['auto_merchant']['merchant_positions']['item name pos'][2],
                        self.data['auto_merchant']['merchant_positions']['item name pos'][3]
                    ])
                    merchant_item_screenshot.save(f"{self.images_path}\\item.png")
                    merchant_item = pytesseract.image_to_string(merchant_item_screenshot)
                    merchant_item = merchant_item.split('|')[0].strip()
                    handle_log_msg("INFO", f"Merchant Item Unchecked: {merchant_item}, Items to Buy: {self.items_to_buy} Python log line 146")

                    checked_merchant_item = self.handle_ocr_miss(merchant_item)
                    handle_log_msg("INFO", f"Merchant Item: {checked_merchant_item}, Items to Buy: {self.items_to_buy} Python log line 149")

                    checked_merchant_item.lower()
                    if checked_merchant_item in self.items_to_buy:
                        if self.init_ref.stop_macro_flag:
                            return
                        handle_log_msg("INFO", f"Purchasing: {checked_merchant_item} Python log line 155")

                        self.amount = self.data['auto_merchant'][checked_merchant_name][checked_merchant_item]['amount']
                        if self.amount == 0:
                            handle_log_msg("INFO", f"Skipping: {checked_merchant_item} because item amount is 0 or less | amount: {self.amount}")
                            continue
                        
                        autoit.mouse_click('left', self.merchant_positions['amount button'][0], self.merchant_positions['amount button'][1], clicks=1)

                        keys = ['^a', str(self.amount), '{enter}']

                        for key in keys:
                            autoit.send(key)
                        
                        autoit.mouse_click('left', self.merchant_positions['purchase button'][0], self.merchant_positions['purchase button'][1])
                        time.sleep(1)

                        self.handle_dialogue(4.25)

                    else:
                        if self.init_ref.stop_macro_flag:
                            return
                        handle_log_msg("INFO", f"Skipping: {checked_merchant_item} (Not in buy list) Python log line 170")

                    first_item_pos_x += 190
                
                if os.path.exists(f"{self.images_path}\\merchant.png"):
                    os.remove(f"{self.images_path}\\merchant.png")
                elif os.path.exists(f"{self.images_path}\\item.png"):
                    os.remove(f"{self.images_path}\\item.png")

                return
            else:
                return "No Merchant Found"


        except Exception as e:
            handle_log_msg("ERROR", f"{e} Python line 185")
            return "ERROR"
        

if __name__ == "__main__":
    test = AutoMerchant()
    test.handle_ocr_miss('mari')