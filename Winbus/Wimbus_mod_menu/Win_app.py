# 3/5/2023
from tkinter import *
from tkinter import ttk
from Wimbus_mod_menu.Winbus_launcher import Launcher_frame


class Win_mod(Tk):
    def __init__(self):
        super().__init__()
        self.title("Winbus Launcher")
        icon_iamge= PhotoImage(file="Winbus_icons\Winmod_icon.png")
        self.iconphoto(False, icon_iamge)
        # Winbus launch tab

        # Note books
        winbus_notebook = ttk.Notebook(self)
        winbus_notebook.pack(expand=1, fill=BOTH)
        
        # Winmod tabs
        winbus_launcher_tab = Launcher_frame(winbus_notebook, self)
        winbus_modding_tab = Frame(winbus_notebook, bg="Blue")

        winbus_notebook.add(winbus_launcher_tab, text="Winbus")
        winbus_notebook.add(winbus_modding_tab, text="Winmod")

win_mod = Win_mod()

win_mod.mainloop()