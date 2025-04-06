import customtkinter as ctk


def showmsg(title, message):
    print(f"showmsg called with title: {title}, message: {message}")

    msg_root = ctk.CTkToplevel()
    msg_root.title(title)
    msg_root.geometry("200x200")
    msg_root.resizable(0, 0)

    msg_root.grid_rowconfigure(0, weight=1)
    msg_root.grid_columnconfigure(0, weight=1)
    msg_root.grid_propagate(0)

    msg = ctk.CTkLabel(msg_root, text=message, wraplength=180)
    msg.grid(row=0, column=0)

    msg.transient()
    msg.grab_set()
    msg.wait_window()


def askyesno(title: str, message: str):
    res = None

    yn = ctk.CTkToplevel()
    yn.title(title)
    yn.geometry("200x200")
    yn.resizable(0, 0)

    yn.grid_rowconfigure((0, 1), weight=1)
    yn.grid_columnconfigure((0, 1), weight=1)
    yn.grid_propagate(0)

    msg = ctk.CTkLabel(yn, text=message, wraplength=180)
    msg.grid(row=0, column=0, sticky='nsew', columnspan=2)

    def yes_action():
        nonlocal res
        res = True
        yn.destroy()

    def no_action():
        nonlocal res
        res = False
        yn.destroy()

    yes_btn = ctk.CTkButton(yn, text="YES", fg_color="#66FF66", text_color="#000000", font=ctk.CTkFont(weight='bold'), width=40, command=yes_action)
    yes_btn.grid(row=1, column=0)

    no_btn = ctk.CTkButton(yn, text="NO", fg_color="#FF6666", text_color="#000000", font=ctk.CTkFont(weight='bold'), width=40, command=no_action)
    no_btn.grid(row=1, column=1)

    yn.transient()
    yn.grab_set()
    yn.wait_window()


    return res