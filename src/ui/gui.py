import customtkinter as ctk
import pathlib
import os
import pathlib

from helpers.helpers import HelperFunctions
from ui.merchant_calibration_ui import MCUI
from ui.auto_potion_settings import APS
from ui.popups import Popup


class UI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.helper = HelperFunctions()
        self.popup = Popup()

        self.config_data = self.helper.load_config()
        self.images_path = os.path.join(pathlib.Path(__file__).parents[2].resolve(), "images")

        self.frames = {
            'Macro': self.create_macro_frame,
            'Settings': self.create_settings_frame,
            'Credits': self.create_credits_frame
        }

        self.tab_buttons = ['Macro', 'Settings', 'Credits']
        self.all_buttons = []

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Nulled Sol's RNG Macro")
        self.geometry("450x250")
        self.config(background="#121212")
        self.iconbitmap(os.path.join(self.images_path, "icon.ico"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_gui()


    def create_gui(self):
        self.main_frame = ctk.CTkFrame(self, width=390, height=240, corner_radius=4, bg_color="#121212", fg_color="#1e1e1e")
        self.main_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_propagate(0)

        self.container_frame = ctk.CTkFrame(self.main_frame, width=380, height=192, bg_color="#1e1e1e", fg_color="#151515", corner_radius=6)
        self.container_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.container_frame.grid_rowconfigure(0, weight=0)
        self.container_frame.grid_rowconfigure(1, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.container_frame.grid_propagate(0)

        self.top_bar = ctk.CTkFrame(self.container_frame, width=380, height=30, fg_color="#131313", bg_color="#151515", corner_radius=0)
        self.top_bar.grid(row=0, column=0, sticky='nsew')
        
        self.top_bar.grid_rowconfigure(0, weight=1)
        self.top_bar.grid_columnconfigure((0, 1, 2), weight=1)

        for idx, btn in enumerate(self.tab_buttons):
            frame_btn = ctk.CTkButton(self.top_bar, 
                text=btn,
                fg_color="#121212", 
                bg_color="#131313",
                hover_color="#151515",
                text_color="#e1e1e1",
                corner_radius=0
            )
            frame_btn.grid(row=0, column=idx, sticky='nsew')
            frame_btn.configure(command=lambda frame=btn, frame_btn=frame_btn: self.swap_frames(frame, frame_btn))

            self.all_buttons.append(frame_btn)
        self.all_buttons[0].configure(fg_color="#151515", state=ctk.DISABLED)
    
        self.create_macro_frame()

        self.bottom_bar = ctk.CTkFrame(self.main_frame, width=380, height=30, corner_radius=6, bg_color="#1e1e1e", fg_color="#131313")
        self.bottom_bar.grid(row=1, column=0, sticky='nsew', pady=(0, 5), padx=5)

        self.bottom_bar.grid_rowconfigure(0, weight=1)
        self.bottom_bar.grid_columnconfigure(0, weight=0)
        self.bottom_bar.grid_columnconfigure(1, weight=0)
        self.bottom_bar.grid_columnconfigure(2, weight=1)
        self.bottom_bar.grid_propagate(0)

        self.start_label = ctk.CTkLabel(self.bottom_bar, text="Start: F1")
        self.start_label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.stop_label = ctk.CTkLabel(self.bottom_bar, text="Stop: F2")
        self.stop_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')


    def swap_frames(self, frame: str, frame_button: ctk.CTkButton):
        for btn in self.all_buttons:
            btn.configure(state='enabled', fg_color="#121212")
        frame_button.configure(state='disabled', fg_color="#151515")

        try:
            self.macro_frame.grid_remove()
            self.settings_frame.grid_remove()
            self.credits_frame.grid_remove()

        except AttributeError:
            pass

        self.frames[frame]()
        

    def update_enabled_status(self, item, checkbox: ctk.CTkCheckBox):
        new_val = checkbox.get()

        self.helper.edit_config([item, 'enabled'], new_val)
    

    def edit_interval(self, event, item_to_edit: str, entry: ctk.CTkEntry):
        new_val = entry.get()

        if item_to_edit == 'biome_randomizer':
            self.biome_randomizer_interval.configure(text=f"Biome Randomizer Interval: {new_val}")
        elif item_to_edit == 'strange_controller':
            self.strange_controller_interval.configure(text=f"Strange Controller Interval: {new_val}")
        elif item_to_edit == 'clip_aura':
            self.clip_aura_keybind_label.configure(text=f"Clip Aura Keybind: {new_val}")
        elif item_to_edit == 'auto_merchant':
            self.merchant_interval.configure(text=f"Merchant Interval: {new_val}")

        self.helper.edit_config([item_to_edit, 'interval'], float(new_val))


    def create_macro_frame(self):
        self.config_data = self.helper.load_config()

        self.macro_frame = ctk.CTkFrame(self.container_frame, fg_color="#151515", corner_radius=0, width=self.container_frame.winfo_width())
        self.macro_frame.grid(row=1, column=0, sticky='nsew', rowspan=2, columnspan=2)

        self.macro_frame.grid_rowconfigure(0, weight=1)
        self.macro_frame.grid_rowconfigure(1, weight=1)
        self.macro_frame.grid_columnconfigure(0, weight=0)
        self.macro_frame.grid_columnconfigure(1, weight=1)
        self.macro_frame.grid_propagate(0)

        self.toggle_container = ctk.CTkFrame(self.macro_frame, fg_color="#151515")
        self.toggle_container.grid(row=0, column=0, padx=10, pady=10, sticky='nw', ipady=5, ipadx=5)

        self.toggle_container.grid_rowconfigure([0, 1, 2, 3], weight=1)
        self.toggle_container.grid_columnconfigure([0, 1], weight=1)
        self.toggle_container.grid_propagate(0)


        self.toggle_auto_randomizer = ctk.CTkCheckBox(self.toggle_container, text="Biome Randomizer", hover_color="#121212", fg_color="#1e1e1e")
        self.toggle_auto_randomizer.grid(row=0, column=0, sticky='nsew')
        self.toggle_auto_randomizer.configure(command=lambda item='biome_randomizer', checkbox=self.toggle_auto_randomizer: self.update_enabled_status(item, checkbox))
        if self.config_data['biome_randomizer']['enabled'] == 1:
            self.toggle_auto_randomizer.select()

        self.auto_randomizer_interval = ctk.CTkEntry(self.toggle_container, width=60)
        self.auto_randomizer_interval.grid(row=0, column=1)
        self.auto_randomizer_interval.insert(ctk.END, self.config_data['biome_randomizer']['interval'])
        self.auto_randomizer_interval.bind('<Return>', command=lambda event, item_to_edit='biome_randomizer', interval=self.auto_randomizer_interval: self.edit_interval(event, item_to_edit, interval))


        self.toggle_auto_controller = ctk.CTkCheckBox(self.toggle_container, text="Strange Controller", hover_color="#121212", fg_color="#1e1e1e")
        self.toggle_auto_controller.grid(row=1, column=0, sticky='nsew')
        self.toggle_auto_controller.configure(command=lambda item='strange_controller', checkbox=self.toggle_auto_controller: self.update_enabled_status(item, checkbox))
        if self.config_data['strange_controller']['enabled'] == 1:
            self.toggle_auto_controller.select()

        self.auto_controller_interval = ctk.CTkEntry(self.toggle_container, width=60)
        self.auto_controller_interval.grid(row=1, column=1)
        self.auto_controller_interval.insert(ctk.END, self.config_data['strange_controller']['interval'])
        self.auto_controller_interval.bind('<Return>', command=lambda event, item_to_edit='strange_controller', interval=self.auto_controller_interval: self.edit_interval(event, item_to_edit, interval))


        self.auto_merchant = ctk.CTkCheckBox(self.toggle_container, text="Auto Merchant", hover_color="#121212", fg_color="#1e1e1e")
        self.auto_merchant.grid(row=2, column=0, sticky='nsew')
        self.auto_merchant.configure(command=lambda item='auto_merchant', checkbox=self.auto_merchant: self.update_enabled_status(item, checkbox))
        if self.config_data['auto_merchant']['enabled'] == 1:
            self.auto_merchant.select()

        self.auto_merchant_interval = ctk.CTkEntry(self.toggle_container, width=60)
        self.auto_merchant_interval.grid(row=2, column=1)
        self.auto_merchant_interval.insert(ctk.END, self.config_data['auto_merchant']['interval'])
        self.auto_merchant_interval.bind('<Return>', command=lambda event, item_to_edit='auto_merchant', interval=self.auto_merchant_interval: self.edit_interval(event, item_to_edit, interval))
        

        self.toggle_detect_auras = ctk.CTkCheckBox(self.toggle_container, text="Detect Auras", hover_color="#121212", fg_color="#1e1e1e")
        self.toggle_detect_auras.grid(row=3, column=0, sticky='nsew')
        self.toggle_detect_auras.configure(command=lambda item='clip_aura', checkbox=self.toggle_detect_auras: self.update_enabled_status(item, checkbox))
        if self.config_data['clip_aura']['enabled'] == 1:
            self.toggle_detect_auras.select()

        self.clip_aura_keybind = ctk.CTkEntry(self.toggle_container, width=60)
        self.clip_aura_keybind.grid(row=3, column=1)
        self.clip_aura_keybind.insert(ctk.END, self.config_data['clip_aura']['clip_hotkey'])
        self.clip_aura_keybind.bind('<Return>', command=lambda event, item_to_edit='clip_aura', interval=self.clip_aura_keybind: self.edit_interval(event, item_to_edit, interval))


        self.toggle_detect_biome = ctk.CTkCheckBox(self.toggle_container, text="Detect Biome", hover_color="#121212", fg_color="#1e1e1e")
        self.toggle_detect_biome.grid(row=4, column=0, sticky='nsew')
        self.toggle_detect_biome.configure(command=lambda item='detect_biome', checkbox=self.toggle_detect_biome: self.update_enabled_status(item, checkbox))
        if self.config_data['detect_biome']['enabled'] == 1:
            self.toggle_detect_biome.select()


        self.other_container = ctk.CTkFrame(self.macro_frame, fg_color="#151515")
        self.other_container.grid(row=0, column=1, padx=10, pady=10, sticky='nw', ipady=5, ipadx=5)

        self.other_container.grid_rowconfigure([0, 1, 2], weight=1)
        self.other_container.grid_columnconfigure(0, weight=1)


        self.biome_randomizer_interval = ctk.CTkLabel(self.other_container, 
            text=f"Biome Randomizer Interval: {self.config_data['biome_randomizer']['interval']}",
        )
        self.biome_randomizer_interval.grid(row=0, column=0)

        self.strange_controller_interval = ctk.CTkLabel(self.other_container, 
            text=f"Strange Controller Interval: {self.config_data['strange_controller']['interval']}"
        )
        self.strange_controller_interval.grid(row=1, column=0)


        self.merchant_interval = ctk.CTkLabel(self.other_container,
            text=f"Merchant Interval: {self.config_data['auto_merchant']['interval']}"
        )
        self.merchant_interval.grid(row=2, column=0)


        self.clip_aura_keybind_label = ctk.CTkLabel(self.other_container, 
            text=f"Clip Aura Keybind: {self.config_data['clip_aura']['clip_hotkey']}"
        )
        self.clip_aura_keybind_label.grid(row=3, column=0)


        self.auto_potion_button = ctk.CTkButton(self.other_container, 
            text="Configure Auto Potion", 
            fg_color="#1c1c1c", 
            hover_color="#1e1e1e",
            font=ctk.CTkFont(weight='bold'),
            command=lambda: APS().auto_potion_settings_ui()
        )
        self.auto_potion_button.grid(row=4, column=0, stick='sew')


    def create_settings_frame(self):
        self.settings_frame = ctk.CTkFrame(self.container_frame, fg_color="#151515", corner_radius=0, width=self.container_frame.winfo_width())
        self.settings_frame.grid(row=1, column=0, sticky='nsew')

        self.settings_frame.grid_rowconfigure([0, 1], weight=1)
        self.settings_frame.grid_columnconfigure(0, weight=1)   
        self.settings_frame.grid_propagate(0)

        self.url_input_frame = ctk.CTkFrame(self.settings_frame, fg_color="#151515")
        self.url_input_frame.grid(row=0, column=0, sticky='new', padx=5, pady=5)

        self.url_input_frame.grid_columnconfigure(1, weight=1)
        self.url_input_frame.grid_propagate(0)

        self.webhook_entry_label = ctk.CTkLabel(self.url_input_frame, text="Webhook URL", font=ctk.CTkFont(weight="bold"))
        self.webhook_entry_label.grid(row=0, column=0, padx=(0, 5), pady=5)

        self.webhook_entry = ctk.CTkEntry(self.url_input_frame, show="*")
        self.webhook_entry.grid(row=0, column=1, sticky='ew', padx=(0, 5))
        self.webhook_entry.bind("<Return>", self.save_webhook_text)
        self.webhook_entry.insert(ctk.END, self.config_data['webhook_url'])

        self.private_server_entry_label = ctk.CTkLabel(self.url_input_frame, text="PS URL", font=ctk.CTkFont(weight="bold"))
        self.private_server_entry_label.grid(row=1, column=0, padx=(0, 5))
    
        self.private_server_entry = ctk.CTkEntry(self.url_input_frame)
        self.private_server_entry.grid(row=1, column=1, sticky='ew', padx=(0, 5))
        self.private_server_entry.bind("<Return>", self.save_ps_text)
        self.private_server_entry.insert(ctk.END, self.config_data['private_server_link'])

        self.merchant_edit_buttons_frame = ctk.CTkFrame(self.settings_frame, fg_color="#151515")
        self.merchant_edit_buttons_frame.grid(row=1, column=0, sticky='sew', padx=5, pady=5)

        self.merchant_edit_buttons_frame.grid_rowconfigure([0, 1], weight=1)
        self.merchant_edit_buttons_frame.grid_columnconfigure([0, 1], weight=1)
        self.merchant_edit_buttons_frame.grid_propagate(0)
        
        self.mari_edit_auto_items_btn = ctk.CTkButton(self.merchant_edit_buttons_frame, 
            text="Edit Mari Items",
            fg_color="#121212",
            hover_color="#1c1c1c",
            command=lambda: MCUI().mari_auto_items_ui())
        self.mari_edit_auto_items_btn.grid(row=0, column=0, sticky='new', padx=5)

        self.jester_edit_auto_items_btn = ctk.CTkButton(self.merchant_edit_buttons_frame, 
            text="Edit Jester Items",
            fg_color="#121212",
            hover_color="#1c1c1c",      
            command=lambda: MCUI().jester_auto_items_ui())
        self.jester_edit_auto_items_btn.grid(row=0, column=1, sticky='new', padx=5)

        self.merchant_calibration_btn = ctk.CTkButton(self.merchant_edit_buttons_frame, 
            text="Edit Merchant Calibration",
            fg_color="#121212",
            hover_color="#1c1c1c",                                          
            command=lambda: MCUI().merchant_calibration_ui())
        self.merchant_calibration_btn.grid(row=1, column=0, columnspan=2, sticky='sew', padx=5, pady=5)


    def save_ps_text(self, event):
        url = self.private_server_entry.get()

        choice = self.popup.askconfirmation(message=f'Are you sure you would like to set "{url}" as your private server link?')
        if choice:
            self.helper.edit_config(['private_server_link'], url)
            return
        self.popup.showinfo(message="PRIVATE SERVER LINK NOT ADDED")


    def save_webhook_text(self, event):
        url = self.webhook_entry.get()
        
        choice = self.popup.askconfirmation(message=f'Are you sure you would like to set "{url}" as your webhook link?')
        if choice:
            self.helper.edit_config(['webhook_url'], url)
            return
        self.popup.showinfo("WEBHOOK LINK NOT ADDED")


    def create_credits_frame(self):
        self.credits_frame = ctk.CTkFrame(self.container_frame, fg_color="#151515", corner_radius=0, width=self.container_frame.winfo_width())
        self.credits_frame.grid(row=1, column=0, sticky='nsew')

        self.test = ctk.CTkLabel(self.credits_frame, text="Credits Frame")
        self.test.grid(row=0, column=0)