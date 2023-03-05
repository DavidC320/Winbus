# 3/2/2023
import pygame
from Player_base import User_team
from Music_manager import Music_manager, Sound_manager
from Card_base import create_card
from misc_funtions import quick_display_text, timer
from Game_data import cards

pygame.init()
pygame.font.init()

class Player_card_pick_sub_menu:
    def __init__(self, player: User_team, x_pos):
        self.player= player
        self.max_cards= [self.player.max_deck, 0]
        
        self.select_index= 0
        self.list_mode= 0

        self.ready = False
        self.sound= Sound_manager("SFX")

        self.card_list= []

        self.selectable_cards = []
        for card_name in cards.get("card units").keys():
            chunk = [create_card(card_name), 0, card_name]
            self.selectable_cards.append(chunk)
        self.card_list.append(self.selectable_cards)

        self.selectable_crowns= []
        for card_name in cards.get("card crowns").keys():
            chunk = [create_card(card_name, "card crowns"), 0, card_name]
            self.selectable_crowns.append(chunk)
        self.selectable_crowns[0][1] = 1
        self.card_list.append(self.selectable_crowns)

        # ui
        self.card_description = pygame.Rect(0, 0, 300, 160)
        self.card_selection = pygame.Rect(0, 0, 400, 500)

        self.card_description.center= (x_pos, 100)
        self.card_selection.center= (x_pos, 430)
        self.x_offset= x_pos

    def set_menu(self):
        self.ready = False

    def display_ui(self, display):
        control_map = self.player.player_control_configuration[1]
        for rect in (self.card_description, self.card_selection):
            pygame.draw.rect(display, "white", rect, 4)
        self.display_selectable_cards(display, 22)
        quick_display_text(display, self.max_cards[self.list_mode], "green", (self.x_offset+ 175, 160))

        if self.ready:
            quick_display_text(display, "%s: Ready!" % control_map.get("use card"), "yellow", (self.x_offset, 750), size=40)
        else:
            quick_display_text(display, "%s: Ready?" % control_map.get("use card"), "White", (self.x_offset, 750), size=40)

    def display_selectable_cards(self, display, font_size):
        card_list = self.card_list[self.list_mode]
        row_height= self.card_selection.height // font_size
        empty_space = self.card_selection.height / row_height

        number_of_rows_available = self.card_selection.height // row_height
        if number_of_rows_available > len(card_list):
            number_of_rows_available = len(card_list)
        y_pos = self.card_selection.top + font_size/2 + empty_space

        start_number = 0
        back_ground= pygame.Rect(0, 0, self.card_selection.width, row_height)
        #print(number_of_rows_available, row_height, empty_space, len(self.selectable_cards))
        for _ in range(int(number_of_rows_available)):
            control_map = self.player.player_control_configuration[1]
            card, number_selected, _ = card_list[start_number]
            back_ground.midleft = (self.card_selection.left, y_pos)

            if start_number == self.select_index:
                pygame.draw.rect(display, "grey", back_ground)
                quick_display_text(display, "- %s" % control_map.get("left"), "white", back_ground.midleft, "midright", back_ground_color= "black")
                quick_display_text(display, "%s +" % control_map.get("right"), "white", back_ground.midright, "midleft", back_ground_color= "black")
            else:
                pygame.draw.rect(display, "black", back_ground)

            quick_display_text(display, " $%s" % card.coin_cost, "purple", (self.card_selection.left+ 5, y_pos), "midleft", font_size, back_ground_color="black")
            quick_display_text(display, card.name, "brown", (self.card_selection.left+ 45, y_pos), "midleft", font_size, back_ground_color="black")
            quick_display_text(display, number_selected, "Green", (self.card_selection.right- 20, y_pos), "midright", font_size, back_ground_color="black")
            start_number += 1
            y_pos += font_size/2 + empty_space

    def add_card_number(self):
        current_card = self.card_list[self.list_mode][self.select_index]
        if self.max_cards[self.list_mode] > 0:
            self.sound.play_sound(2)
            self.max_cards[self.list_mode] -= 1
            current_card[1] += 1
        else:
            self.sound.play_sound(1)

    def sub_card_number(self):
        current_card = self.card_list[self.list_mode][self.select_index]
        if current_card[1] > 0:
            self.sound.play_sound(2)
            self.max_cards[self.list_mode] += 1
            current_card [1]-= 1
        else:
            self.sound.play_sound(1)

    def set_deck(self):
        self.player.init_deck.clear()

        for _, number, card_name in self.card_list[0]:
            for _ in range(number):
                self.player.init_deck.append(card_name)

        for _, number, card_name in self.card_list[1]:
            if number > 0:
                self.player.crown = card_name
                break
        
        print(self.player.init_deck)

    def change_index(self, number):
        self.select_index += number
        if self.select_index >= len(self.card_list[self.list_mode]):
            self.select_index = 0
        elif self.select_index < 0:
            self.select_index = len(self.card_list[self.list_mode]) - 1

    def change_mode(self, number):
        self.sound.play_sound(3)
        self.list_mode += 1
        if self.list_mode >= len(self.card_list):
            self.list_mode = 0
        elif self.list_mode < 0:
            self.list_mode = len(self.card_list) - 1
        self.change_index(0)

    def controls(self, event):
        control = self.player.player_control_configuration[0]

        if event.type == pygame.KEYDOWN:
            if event.key == control.get("up"):
                self.change_index(-1)

            elif event.key == control.get("down"):
                self.change_index(1)

            elif event.key == control.get("left"):
                self.sub_card_number()

            elif event.key == control.get("right"):
                self.add_card_number()

            elif event.key == control.get("last card"):
                self.change_mode(-1)

            elif event.key == control.get("next card"):
                self.change_mode(1)

            elif event.key == control.get("use card"):
                if self.ready:
                    self.ready = False
                else:
                    self.ready = True


class Deck_builder_menu:
    def __init__(self, display, clock, player_1, player_2, main):
        self.display= display
        self.clock= clock
        self.current_time= 0
        self.main = main

        self.player_1= player_1
        self.player_2= player_2
        self.player_1_menu = Player_card_pick_sub_menu(self.player_1, 280)
        self.player_2_menu = Player_card_pick_sub_menu(self.player_2, 920)

        self.waiting= False
        self.play_ready= False
        self.ready_start_time= 0
        self.read_limit= 0
        self.music= Music_manager(r"Music")
        self.sound= Sound_manager(r"SFX")

    def set_menu(self):
        self.read_limit = 0
        self.player_1_menu.set_menu()
        self.player_2_menu.set_menu()
        self.music.play_index_music(1)

    def display_ui(self):
        for menu in (self.player_1_menu, self.player_2_menu):
            menu.display_ui(self.display)

        if self.waiting:
            size = self.display.get_size()
            if self.read_limit >= 3:
                quick_display_text(self.display, "You can't back out!", "red", [size[0]/2, size[1]/2-10], size=30)
            quick_display_text(self.display, "Next round in...", "yellow", [size[0]/2, size[1]/2 + 20], size=30)
            quick_display_text(self.display, f"{int((self.current_time - self.ready_start_time)/1000)} seconds" , "yellow", [size[0]/2, size[1]/2 + 70], size=40)

    def player_event_controls(self, event):
        for player in (self.player_1_menu, self.player_2_menu):
            player.controls(event)

    def ready_fight(self):
        if self.player_1_menu.ready and self.player_2_menu.ready and not self.waiting:
            self.waiting = True
            self.ready_start_time = self.current_time
            self.play_ready = True
            self.read_limit += 1

        elif (not self.player_1_menu.ready or not self.player_2_menu.ready) and not self.read_limit >= 3:
            self.waiting = False

        if self.play_ready:
            self.play_ready = False
            self.sound.play_sound(0)

        if timer(self.ready_start_time, 5, self.current_time) and self.waiting:
            self.player_1_menu.set_deck()
            self.player_2_menu.set_deck()
            self.main.game_state= "setup combat"

    def display_decks(self):
        pass

    def play_menu(self):
        self.current_time= pygame.time.get_ticks()
        self.display.fill("Black")

        quick_display_text(self.display, "Select your cards!", "Yellow", (600, 40), size=40)

        self.ready_fight()

        self.display_ui()