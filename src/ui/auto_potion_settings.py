import customtkinter as ctk

from helpers.helpers import HelperFunctions


class APS:
    def __init__(self):
        self.helper = HelperFunctions()
    

    def toggle_potion_enabled(self, potion, checkbox: ctk.CTkCheckBox):
        new_val = checkbox.get()
        
        self.helper.edit_config(['auto_potion', 'potions', potion, 'enabled'], new_val)

    
    def enable_auto_potion(self, checkbox: ctk.CTkCheckBox):
        val = checkbox.get()

        self.helper.edit_config(['auto_potion', 'enabled'], val)
    
    
    def edit_interval(self, event):
        try:
            new_interval = self.potion_craft_swap_interval.get()
            
            self.helper.edit_config(['auto_potion', 'swap_interval'], float(new_interval))
        
        except ValueError:
            return

    
    def auto_potion_settings_ui(self):
        self.data = self.helper.load_config()

        ui = ctk.CTkToplevel()
        ui.geometry('200x260')
        ui.title("Auto Potion Settings")

        ui.grid_rowconfigure(0, weight=1)
        ui.grid_columnconfigure(0, weight=1)

        toggle_potion_frame = ctk.CTkFrame(ui)
        toggle_potion_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ns')

        toggle_potion_frame.grid_propagate(0)

        for idx, potion in enumerate(self.data['auto_potion']['potions']):

            potion_checkbox = ctk.CTkCheckBox(toggle_potion_frame, text=potion, hover_color="#121212", fg_color="#1e1e1e")
            potion_checkbox.grid(row=idx, column=0, padx=5, pady=5)

            if self.data['auto_potion']['potions'][potion]['enabled'] == 1:
                potion_checkbox.select()

            potion_checkbox.configure(command=lambda potion=potion, checkbox=potion_checkbox: self.toggle_potion_enabled(potion, checkbox))

        potion_settings_frame = ctk.CTkFrame(ui)
        potion_settings_frame.grid(row=1, column=0, padx=5, pady=5, stick='sew', ipadx=5, ipady=5)

        potion_settings_frame.grid_rowconfigure(0, weight=1)
        potion_settings_frame.grid_columnconfigure([0, 1], weight=1)

        enable_auto_potion = ctk.CTkCheckBox(potion_settings_frame, text="Auto Potion", hover_color="#121212", fg_color="#1e1e1e")
        enable_auto_potion.grid(row=0, column=0)
        if self.data['auto_potion']['enabled'] == 1:
            enable_auto_potion.select()
        enable_auto_potion.configure(command=lambda checkbox=enable_auto_potion: self.enable_auto_potion(checkbox))

        self.potion_craft_swap_interval = ctk.CTkEntry(potion_settings_frame, width=60)
        self.potion_craft_swap_interval.grid(row=0, column=1, stick='e', padx=(0, 5))
        self.potion_craft_swap_interval.insert(ctk.END, self.data['auto_potion']['swap_interval'])
        self.potion_craft_swap_interval.bind('<Return>', command=self.edit_interval)

        ui.transient()
        ui.grab_set()