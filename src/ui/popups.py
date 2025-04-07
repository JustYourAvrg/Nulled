import customtkinter as ctk

# from src.helpers.helpers import HelperFunctions

class Popup:
    def __init__(self):
        pass


    def showinfo(self, message: str):
        self.info_root = ctk.CTkToplevel()
        self.info_root.geometry('250x150')
        self.info_root.title('INFO')

        self.info_root.grid_rowconfigure(0, weight=1)
        self.info_root.grid_columnconfigure(0, weight=1)

        self.info_message_frame = ctk.CTkFrame(self.info_root)
        self.info_message_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.info_message_frame.grid_rowconfigure(0, weight=1)
        self.info_message_frame.grid_columnconfigure(0, weight=1)

        self.info_message = ctk.CTkLabel(self.info_message_frame, 
            text_color="#fafafa",
            wraplength=156,
            text=message
        )
        self.info_message.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        self.info_root.transient()
        self.info_root.grab_set()


    def showerror(self, message: str):
        self.error_root = ctk.CTkToplevel()
        self.error_root.geometry('250x150')
        self.error_root.title('ERROR')

        self.error_root.grid_rowconfigure(0, weight=1)
        self.error_root.grid_columnconfigure(0, weight=1)

        self.error_message_frame = ctk.CTkFrame(self.error_root)
        self.error_message_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.error_message_frame.grid_rowconfigure(0, weight=1)
        self.error_message_frame.grid_columnconfigure(0, weight=1)

        self.error_message = ctk.CTkLabel(self.error_message_frame, 
            text_color="#fafafa",
            wraplength=156,
            text=message
        )
        self.error_message.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.error_root.transient()
        self.error_root.grab_set()
    

    def askconfirmation(self, message: str):
        self.confirm_root = ctk.CTkToplevel()
        self.confirm_root.geometry('250x150')
        self.confirm_root.title('CONFIRMATION')
        
        self.confirm_root.grid_rowconfigure(0, weight=1)
        self.confirm_root.grid_columnconfigure(0, weight=1)

        self.confirm_frame = ctk.CTkFrame(self.confirm_root)
        self.confirm_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.confirm_frame.grid_rowconfigure(0, weight=1)
        self.confirm_frame.grid_rowconfigure(1, weight=0)
        self.confirm_frame.grid_columnconfigure([0, 1], weight=1)
        self.confirm_frame.grid_propagate(0)

        self.confirm_message = ctk.CTkLabel(self.confirm_frame,
            text_color="#fafafa",
            wraplength=180,
            text=message
        )
        self.confirm_message.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.confirm_button = ctk.CTkButton(self.confirm_frame, 
            width=50,
            text='Confirm',
            fg_color='#141414',
            hover_color='#1c1c1c'
        )
        self.confirm_button.grid(row=1, column=0, padx=5, pady=5, sticky='sew')
        self.confirm_button.configure(command=lambda val='confirm': self.handle_confirmation(val))

        self.deny_button = ctk.CTkButton(self.confirm_frame, 
            width=50,
            text='Deny',
            fg_color='#141414',
            hover_color='#1c1c1c'
        )
        self.deny_button.grid(row=1, column=1, padx=5, pady=5, sticky='sew')
        self.deny_button.configure(command=lambda val='deny': self.handle_confirmation(val))

        self.confirm_root.transient()
        self.confirm_root.grab_set()
        self.confirm_root.wait_window()
        
        return self.return_val
    

    def handle_confirmation(self, value):
        try:
            if value == 'confirm':
                self.confirm_root.destroy()
                self.return_val = True
            
            elif value == 'deny':
                self.confirm_root.destroy()
                self.return_val = False
        
        except Exception as e:
            self.return_val = e


if __name__ == '__main__':
    test = Popup()
    test.askconfirmation('Would you like to set "https://example.com" as your webhook URL?')