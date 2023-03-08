# 3/5/2023
from tkinter import *

class Win_mod(Tk):
    def __init__(self):
        super().__init__()
        self.title("Winmod")

        Label(self, text="Winmod").pack()
        Label(self, text="Version: Alpha 0.0").pack()

win_mod = Win_mod()

win_mod.mainloop()