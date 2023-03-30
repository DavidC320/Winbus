# 3/3/2023

from pygame import mixer
from random import choice
import os

mixer.init()

class Sound_manager:
    def __init__(self, folder):
        self.sfx_list = []
        self.grab_sfx(folder)

    def grab_sfx(self, folder):
        music = []
        music_folder = folder
        for file in os.listdir(music_folder):
            file_path = music_folder+ "\\"+ file
            sound =  mixer.Sound(file_path)
            music.append(sound)
        self.sfx_list = music

    def play_sound(self, index, volume=.6):
        self.sfx_list[index].set_volume(volume)
        self.sfx_list[index].play()

class Music_manager:
    def __init__(self, folder):
        self.music_list = []
        self.grab_music(folder)


    def grab_music(self, folder):
        music = []
        music_folder = folder
        for file in os.listdir(music_folder):
            file_path = music_folder + "\\" + file
            music.append(file_path)
        self.music_list = music

    def stop_music(self):
        mixer.music.stop()

    def play_index_music(self, index, volume=.4):
        self.stop_music()
        if index >= len(self.music_list):
            index = len(self.music_list) -1
        music_choice = self.music_list[index]
        mixer.music.load(music_choice)
        mixer.music.set_volume(volume)
        mixer.music.play(-1)

    def play_music(self, volume=.4):
        self.stop_music()
        music_choice = choice(self.music_list)
        mixer.music.load(music_choice)
        mixer.music.set_volume(volume)
        mixer.music.play(-1)