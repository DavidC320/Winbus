# 3/2/2023
import pygame
from Player_base import User_team
from Music_manager import Music_manager
from misc_funtions import timer, quick_display_text

pygame.init()
pygame.font.init()


class Combat:
    def __init__(self, display, clock, player_1: User_team, player_2: User_team, main):
        self.display = display
        self.clock = clock
        self.current_time = 0
        self.main = main

        self.music = Music_manager("Music\\battle")
        self.music_r = Music_manager("Music\\rush")
        self.music_w = Music_manager("Music\\win")

        # ui
        self.battle_field = (pygame.Rect(0, 0, 1200, 400), "white")
        self.player_1_field = (pygame.Rect(0, 0, 600, 400), "red")
        self.player_2_field = (pygame.Rect(600, 0, 600, 400), "blue")

        # teams
        self.player_1 = player_1
        self.player_2 = player_2

        # game state
        self.game_state = "fight"
        self.winner_text = "Draw"

        # timers
        self.rush_down = 120
        self.show_winner = 4
        self.next_round = 10
        self.update_unit_speed = .2

        # start times
        self.game_start = 0
        self.show_start = 0
        self.update_start = 0

    def check_dead_team(self):
        p1, p2 = self.player_1.team_dead(), self.player_2.team_dead()
        if p1 and p2:
            self.winner_text = "It's a draw."
            return True
        elif p1:
            self.winner_text = "Player 2!"
            return True
        elif p2:
            self.winner_text = "Player 1"
            return True
        else:
            return False
        
    ###########
    # setting #
    def set_up_teams(self):
        self.music.play_music()
        self.current_time = pygame.time.get_ticks()
        self.game_start = self.current_time
        self.update_start = self.current_time
        self.game_state = "fight"
        self.player_1.set_up_decks([100, 200], self.current_time, self.battle_field[0], self.player_1_field[0],
                                   "#ab6767")
        self.player_2.set_up_decks([1100, 200], self.current_time, self.battle_field[0], self.player_2_field[0],
                                   "#6668aa")

    def team_move(self):
        for team, velocity, opposing_units in (
            (self.player_1, [1, 0], self.player_2.field_units), 
            (self.player_2, [-1, 0], self.player_1.field_units)
        ):

            team.generate_coins(self.current_time)
            team.move_field_units(velocity)

            team.check_field_units(opposing_units, self.current_time)
            if timer(self.update_start, self.update_unit_speed, self.current_time):
                team.update_field_units(opposing_units, self.current_time, self.game_state)

    def change_game_state(self):
        if self.check_dead_team() and self.game_state != "finished":
            self.music_w.play_music()
            self.game_state = "finished"
            self.show_start = self.current_time

        elif self.game_state == "finished" and timer(self.show_start, self.next_round, self.current_time):
            self.game_start = self.current_time
            self.main.game_state = "setup deck"

        elif timer(self.game_start, self.rush_down, self.current_time) and self.game_state not in ("rush", "finished"):
            self.game_state = "rush"
            self.music_r.play_music()
    # setting #
    ###########

    ##############
    # controller #

    def control_function(self, event):
        if self.game_state != "finished":
            self.team_control(event)

    def team_control(self, event):
        for team in (self.player_1, self.player_2):
            team.player_controller(event)

    def team_cursor_controller(self):
        for team in (self.player_1, self.player_2):
            team.current_time = self.current_time - self.game_start
            team.player_cursor_controller()
    # controller #
    ##############

    ###########
    # display #
    def display_team_units(self):
        for team, deck_pos in ((self.player_1, (300, 700)), (self.player_2, (900, 700))):
            team.display_field_units(self.display, self.current_time)
            team.cursor.display_cursor(self.display)
            team.display_held_cards(self.display, deck_pos)

    def display_team_data(self):
        for field, team in ((self.player_1_field, self.player_1), (self.player_2_field, self.player_2)):
            x, y = field[0].center
            y += 220
            pos = [x, y]
            quick_display_text(self.display, f"coins: {team.coins}", "white", pos)
            y += 20
            pos = [x, y]
            quick_display_text(self.display, f"Deck: {len(team.deck)}", "white", pos)
            y += 20
            pos = [x, y]
            quick_display_text(self.display, f"discard: {len(team.discard_pile)}", "white", pos)

    def display_rectangles(self):
        pygame.draw.rect(self.display, "#464d43", self.battle_field[0])
        for rect, color in [self.battle_field, self.player_1_field, self.player_2_field]:
            pygame.draw.rect(self.display, color, rect, 2)

    def display_ui(self):
        self.display.fill("Black")
        self.display_rectangles()
        self.display_team_units()
        quick_display_text(self.display, int((self.current_time - self.game_start)/1000), "white", [600, 430])
        self.display_team_data()
        if self.game_state == "finished":
            x, y = self.display.get_size()
            quick_display_text(self.display, "Finished, The winner is...", "Yellow", [x/2, y/2 - 50], size=40,
                               back_ground_color="black")
            if timer(self.show_start, self.show_winner, self.current_time):
                quick_display_text(self.display, self.winner_text, "Yellow", [x/2, y/2 + 40], size=40,
                                   back_ground_color="black")

        pygame.display.update()
    # display #
    ###########

    def play_combat(self):
        self.change_game_state()
        self.current_time = pygame.time.get_ticks()

        if self.game_state != "finished":
            self.team_cursor_controller()
            
            self.team_move()

        self.display_ui()
