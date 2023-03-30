# 3/3/2023
import pygame
from misc_funtions import quick_display_text
from Player_base import User_team
from Combat import Combat
from Menus import Deck_builder_menu

class Main:
    def __init__(self):
        pygame.display.set_caption("Winbus")
        self.screen_size = [1200, 800]
        self.display = pygame.display.set_mode(self.screen_size)
        icon = pygame.image.load("Data\Sprites\Winbus_icon.png")
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()
        self.player_1 = User_team("player 1", "player_1")
        self.player_2 = User_team("player 2", "player_2")

        # classes
        self.combat = Combat(self.display, self.clock, self.player_1, self.player_2, self)
        self.deck_menu = Deck_builder_menu(self.display, self.clock, self.player_1, self.player_2, self)

        self.game_state = "setup deck"
        self.running= True
        self.debug = False

    def event_controller(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_state == "deck":
                self.deck_menu.player_event_controls(event)

            elif self.game_state == "combat":
                self.combat.control_function(event)
         

    def play_game(self):    
        pygame.init()
        while self.running:
            self.clock.tick(60)
            self.event_controller()

            if self.game_state == "setup deck":
                self.deck_menu.set_menu()
                self.game_state = "deck"
            elif self.game_state == "deck":
                self.deck_menu.play_menu()
            elif self.game_state == "setup combat":
                self.combat.set_up_teams()
                self.game_state = "combat"
            elif self.game_state == "combat":
                self.combat.play_combat()
            else:
                quick_display_text(self.display, "!Something went wrong!", "black", (600, 400), size=80, back_ground_color= "red")

            pygame.display.update()

game = Main()
game.play_game()