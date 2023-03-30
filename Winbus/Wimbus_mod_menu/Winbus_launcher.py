# 3/20/2023
from tkinter import *
from tkinter import ttk
from Back_end_files.Winbus_main import Main

class Launcher_frame(ttk.Frame):
    def __init__(self, container, master):
        super().__init__(container)
        self._master = master
        Label(self, text="Winbus", font=("Gill Sans", 30)).pack(padx=60)
        Label(self, text="Version 1.6.1", font=("Gill Sans", 15)).pack()
        Label(self, text="Status and Effects").pack()

        # Modding
        mod_frame = Frame(self, relief=RIDGE, border=6)
        mod_frame.pack()
        Label(mod_frame, text="Card Packs", relief="sunken").pack(fill=BOTH)
        mod_list = Listbox(mod_frame, selectmode=MULTIPLE)
        mod_list.pack()
        change_folder_btn = Button(mod_frame, text="Change folder", bg="orange").pack(fill=BOTH)
        refresh_button = Button(mod_frame, text="Refresh", bg= "Green").pack(fill=BOTH)

        play_winbus = Button(self, text="play winbus", font=("Ariel", 18), command=self.play_win).pack()
        open_manuel = Button(self, text="Open Manuel").pack()

        # main game
        self.game = Main()

    def play_win(self):
        self._master.withdraw()
        self.game.play_game()
        self._master.destroy()
        