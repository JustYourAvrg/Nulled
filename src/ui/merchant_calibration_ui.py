import customtkinter as ctk

from helpers.helpers import HelperFunctions
from src.ui.popups import Popup
from pynput.mouse import Controller

mouse = Controller


class MCUI:
    def __init__(self):
        self.helper = HelperFunctions()
        self.popup = Popup()
    

    def update_config(self):
        new_input_field_data = {
            "open button": [],
            "dialogue box": [],
            "amount button": [],
            "purchase button": [],
            "first item pos": [],
            "merchant name pos": [],
            "item name pos": []
        }

        for idx, pos in enumerate(self.pos_entry_list):
            x_value = self.pos_entry_list[pos][0].get()
            y_value = self.pos_entry_list[pos][1].get()

            print(pos)
            if pos in ["merchant name pos", "item name pos"]:
                x_value = self.pos_entry_list[pos][0].get()
                y_value = self.pos_entry_list[pos][1].get()

                width_value = self.pos_entry_list[pos][2].get()
                height_value = self.pos_entry_list[pos][3].get()

                new_input_field_data[pos] = [int(x_value), int(y_value), int(width_value), int(height_value)]
            else:
                new_input_field_data[pos] = [int(x_value), int(y_value)]

        self.helper.edit_config(['auto_merchant', 'merchant_positions'], new_input_field_data)
        self.popup.showinfo('Merchant Calibration config saved')


    def select_ss_area(self, thing_to_press):
        self.popup.showinfo(f'Please select the area for {thing_to_press} after closing this popup | NOT YET MADE |')


    def select_pos(self, thing_to_press):
        self.popup.showinfo(f'Please press on the {thing_to_press} after closing this popup | NOT YET MADE |')


    def merchant_calibration_ui(self):
        data = self.helper.load_config()

        calibration_ui = ctk.CTkToplevel()
        calibration_ui.geometry('500x500')
        calibration_ui.title('Merchant Calibration')

        calibration_ui.grid_rowconfigure(0, weight=1)
        calibration_ui.grid_columnconfigure(0, weight=1)

        merchant_pos_frame = ctk.CTkFrame(calibration_ui)
        merchant_pos_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        merchant_pos_frame.grid_columnconfigure([0, 1, 2, 3, 4, 5], weight=1)
        merchant_pos_frame.grid_propagate(0)

        merchant_pos = data['auto_merchant']['merchant_positions']

        self.pos_entry_list = {}
        for idx, pos in enumerate(merchant_pos):
            pos_label = ctk.CTkLabel(merchant_pos_frame, text=pos)
            pos_label.grid(row=idx, column=0, padx=5, stick='w')

            pos_entry_x = ctk.CTkEntry(merchant_pos_frame, width=60)
            pos_entry_x.grid(row=idx, column=1, padx=5)
            pos_entry_x.insert(ctk.END, merchant_pos[pos][0])

            pos_entry_y = ctk.CTkEntry(merchant_pos_frame, width=60)
            pos_entry_y.grid(row=idx, column=2, padx=5)
            pos_entry_y.insert(ctk.END, merchant_pos[pos][1])

            if pos in ['merchant name pos', 'item name pos']:
                pos_entry_width = ctk.CTkEntry(merchant_pos_frame, width=60)
                pos_entry_width.grid(row=idx, column=3)
                pos_entry_width.insert(ctk.END, merchant_pos[pos][2])

                pos_entry_height = ctk.CTkEntry(merchant_pos_frame, width=60)
                pos_entry_height.grid(row=idx, column=4)
                pos_entry_height.insert(ctk.END, merchant_pos[pos][3])

                select_pos_button = ctk.CTkButton(merchant_pos_frame, text="Select POS",
                    fg_color="#1c1c1c",
                    hover_color="#1e1e1e",
                    width=60,
                    command=lambda btn=pos: self.select_ss_area(btn)
                )
                select_pos_button.grid(row=idx, column=5)

                self.pos_entry_list[pos] = (pos_entry_x, pos_entry_y, pos_entry_width, pos_entry_height)

            else:
                select_pos_button = ctk.CTkButton(merchant_pos_frame, text="Select POS",
                    fg_color="#1c1c1c",
                    hover_color="#1e1e1e",
                    width=60,
                    command=lambda btn=pos: self.select_pos(btn)
                )
                select_pos_button.grid(row=idx, column=3)
                self.pos_entry_list[pos] = (pos_entry_x, pos_entry_y)

            merchant_pos_frame.grid_rowconfigure(idx, weight=1)

        
        update_button = ctk.CTkButton(calibration_ui, text="Save Config",
            fg_color="#1c1c1c",
            hover_color="#1e1e1e",
            command=lambda: self.update_config()
        )
        update_button.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        calibration_ui.transient()
        calibration_ui.grab_set()


    def save_mari_item(self, selected_item, checkbox: ctk.CTkCheckBox):
        value = checkbox.get()

        self.helper.edit_config(['auto_merchant', 'mari', selected_item, 'enabled'], value)
    

    def save_jester_item(self, selected_item, checkbox: ctk.CTkCheckBox):
        value = checkbox.get()

        self.helper.edit_config(['auto_merchant', 'jester', selected_item, 'enabled'], value)


    def save_items_amount_data(self, merchant_name):
        if merchant_name == 'mari':
            amount_dict = self.mari_amount_entries.items()
        elif merchant_name == 'jester':
            amount_dict = self.jester_amount_entries.items()

        for item, entry in amount_dict:
            new_amount = entry.get()
            self.helper.edit_config(['auto_merchant', merchant_name, item, 'amount'], new_amount)


    def mari_auto_items_ui(self):
        data = self.helper.load_config()

        mari_ui = ctk.CTkToplevel()
        mari_ui.geometry('420x280')
        mari_ui.title("Mari Items Edit")

        mari_ui.grid_rowconfigure(0, weight=1)
        mari_ui.grid_columnconfigure(0, weight=1)

        options_frame = ctk.CTkFrame(mari_ui)
        options_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        options_frame.grid_propagate(0)

        self.mari_amount_entries = {}
        
        mari_items = data['auto_merchant']['mari']
        for idx, item in enumerate(mari_items):
            row = idx // 2
            col = idx % 2 * 2
            
            item_checkbox = ctk.CTkSwitch(options_frame, text=item, fg_color="#2F2F2F", progress_color="#5C6B7A")
            item_checkbox.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            item_checkbox.configure(command=lambda selected_item=item, checkbox=item_checkbox: self.save_mari_item(selected_item, checkbox))
            if data['auto_merchant']['mari'][item]['enabled'] == 1:
                item_checkbox.select()

            item_amount_entry = ctk.CTkEntry(options_frame, placeholder_text="Amount", width=60)
            item_amount_entry.grid(row=row, column=col + 1, padx=5, pady=5, sticky='ew')
            item_amount_entry.insert(ctk.END, data['auto_merchant']['mari'][item]['amount'])
            item_amount_entry.grid_propagate(0)

            self.mari_amount_entries[item] = item_amount_entry

        save_config_button = ctk.CTkButton(mari_ui, 
            text="Save Config", 
            fg_color="#141414",
            hover_color="#121212",
            command=lambda: self.save_items_amount_data('mari')
        )
        save_config_button.grid(row=1, column=0, padx=5, pady=(0, 5), stick='nsew')

        mari_ui.transient()
        mari_ui.grab_set()


    def jester_auto_items_ui(self):
        data = self.helper.load_config()

        jester_ui = ctk.CTkToplevel()
        jester_ui.geometry('450x350')
        jester_ui.title("Jester Items Edit")

        jester_ui.grid_rowconfigure(0, weight=1)
        jester_ui.grid_columnconfigure(0, weight=1)

        options_frame = ctk.CTkFrame(jester_ui)
        options_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        options_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        options_frame.grid_propagate(0)

        self.jester_amount_entries = {}
        
        jester_items = data['auto_merchant']['jester']
        for idx, item in enumerate(jester_items):
            row = idx // 2
            col = idx % 2 * 2
            
            item_checkbox = ctk.CTkSwitch(options_frame, text=item, fg_color="#2F2F2F", progress_color="#5C6B7A")
            item_checkbox.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            item_checkbox.configure(command=lambda selected_item=item, checkbox=item_checkbox: self.save_jester_item(selected_item, checkbox))
            if data['auto_merchant']['jester'][item]['enabled'] == 1:
                item_checkbox.select()

            item_amount_entry = ctk.CTkEntry(options_frame, placeholder_text="Amount", width=60)
            item_amount_entry.grid(row=row, column=col + 1, padx=5, pady=5, sticky='ew')
            item_amount_entry.insert(ctk.END, data['auto_merchant']['jester'][item]['amount'])
            item_amount_entry.grid_propagate(0)

            self.jester_amount_entries[item] = item_amount_entry

            options_frame.grid_rowconfigure(row, weight=1)

        save_config_button = ctk.CTkButton(jester_ui, 
            text="Save Config", 
            fg_color="#141414",
            hover_color="#121212",
            command=lambda: self.save_items_amount_data('jester')
        )
        save_config_button.grid(row=1, column=0, padx=5, pady=(0, 5), stick='nsew')

        jester_ui.transient()
        jester_ui.grab_set()