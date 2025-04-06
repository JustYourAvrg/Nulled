import customtkinter as ctk

from helpers.helpers import HelperFunctions


class MCUI:
    def __init__(self):
        self.helper = HelperFunctions()
    

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

        for idx, pos in enumerate(self.merchant_entries):
            x_value = self.merchant_entries[pos][0].get()
            y_value = self.merchant_entries[pos][1].get()

            if pos in ["merchant name pos", "item name pos"]:
                width_value = self.merchant_entries[pos][2].get()
                height_value = self.merchant_entries[pos][3].get()

                new_input_field_data[pos] = [int(x_value), int(y_value), int(width_value), int(height_value)]
            else:
                new_input_field_data[pos] = [int(x_value), int(y_value)]

        self.helper.edit_config(['auto_merchant', 'merchant_positions'], new_input_field_data)
    

    def save_mari_item(self, selected_item, checkbox: ctk.CTkCheckBox):
        value = checkbox.get()

        self.helper.edit_config(['auto_merchant', 'mari', selected_item, 'enabled'], value)
    

    def save_jester_item(self, selected_item, checkbox: ctk.CTkCheckBox):
        value = checkbox.get()

        self.helper.edit_config(['auto_merchant', 'jester', selected_item, 'enabled'], value)


    def merchant_calibration_ui(self):
        data = self.helper.load_config()    

        merchant_ui = ctk.CTkToplevel()
        merchant_ui.geometry('350x300')
        merchant_ui.title("Merchant Calibration")

        merchant_ui.grid_rowconfigure(0, weight=1)
        merchant_ui.grid_columnconfigure(0, weight=1)

        pos_frame = ctk.CTkFrame(merchant_ui)
        pos_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        pos_frame.grid_rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)
        pos_frame.grid_columnconfigure([0, 1, 2, 3, 4], weight=1)
        pos_frame.grid_propagate(0)

        self.merchant_entries = {}

        merchant_positions = data['auto_merchant']['merchant_positions']
        for idx, pos in enumerate(merchant_positions):
            pos_label = ctk.CTkLabel(pos_frame, text=pos)
            pos_label.grid(row=idx, column=0)

            pos_input_x = ctk.CTkEntry(pos_frame, placeholder_text="X", width=50)
            pos_input_x.grid(row=idx, column=1)
            pos_input_x.insert(ctk.END, merchant_positions[pos][0])

            pos_input_y = ctk.CTkEntry(pos_frame, placeholder_text="Y", width=50)
            pos_input_y.grid(row=idx, column=2)
            pos_input_y.insert(ctk.END, merchant_positions[pos][1])

            if pos in ["merchant name pos", "item name pos"]:
                pos_input_width = ctk.CTkEntry(pos_frame, placeholder_text="Width", width=50)
                pos_input_width.grid(row=idx, column=3)
                pos_input_width.insert(ctk.END, merchant_positions[pos][2])

                pos_input_height = ctk.CTkEntry(pos_frame, placeholder_text="Height", width=50)
                pos_input_height.grid(row=idx, column=4)
                pos_input_height.insert(ctk.END, merchant_positions[pos][3])

                self.merchant_entries[pos] = [pos_input_x, pos_input_y, pos_input_width, pos_input_height]

            else:
                self.merchant_entries[pos] = [pos_input_x, pos_input_y]


        save_config_button = ctk.CTkButton(merchant_ui, 
            text="Save Config", 
            fg_color="#141414",
            hover_color="#121212",
            command=lambda: self.update_config()
        )
        save_config_button.grid(row=1, column=0, padx=5, pady=(0, 5), stick='nsew')

        merchant_ui.transient()
        merchant_ui.grab_set()
    

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
        mari_ui.geometry('400x300')
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
            
            item_checkbox = ctk.CTkCheckBox(options_frame, text=item, hover_color="#121212", fg_color="#1e1e1e")
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
            
            item_checkbox = ctk.CTkCheckBox(options_frame, text=item, hover_color="#121212", fg_color="#1e1e1e")
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