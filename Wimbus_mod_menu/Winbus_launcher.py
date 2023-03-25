# 3/20/2023
from tkinter import *
from tkinter import ttk

class Launcher_frame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        Label(self, text="HI").pack()
        