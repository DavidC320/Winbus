# 2/20/2023
import pygame
from Player_base import User_team
from misc_funtions import timer, quick_display_text

pygame.init()
pygame.font.init()


class Winbus:
    def __init__(self):
        pygame.display.set_caption("Winbus")
        self.screen_size= [1200, 800]
        self.display= pygame.display.set_mode(self.screen_size)
        self.clock= pygame.time.Clock()
        self.current_time= 0

        # ui
        self.battle_field= (pygame.Rect(0, 0, 1200, 400), "white")
        self.player_1_field= (pygame.Rect(0, 0, 600, 400), "red")
        self.player_2_field= (pygame.Rect(600, 0, 600, 400), "blue")

        # teams
        self.player_1= User_team("player 1", "player_1")
        self.player_2= User_team("player 2", "player_2")

        # game state
        self.game_state= "fight"
        self.winner_text= "Draw"

        #timers
        self.rush_down= 120
        self.show_winner= 4
        self.next_round= 10

        # start times
        self.game_start= 0
        self.show_start= 0

    def check_dead_team(self):
        p1, p2 = self.player_1.team_dead(), self.player_2.team_dead()
        if p1 and p2:
            self.winner_text= "It's a draw."
            return True
        elif p1:
            self.winner_text= "Player 2!"
            return True
        elif p2:
            self.winner_text= "Player 1"
            return True
        else:
            return False

    def change_game_state(self):
        if self.check_dead_team() and self.game_state != "finished":
            self.game_state= "finished"
            self.show_start= self.current_time

        elif self.game_state == "finished" and timer(self.show_start, self.next_round, self.current_time):
            self.game_start = self.current_time
            self.set_up_teams()

        elif timer(self.game_start, self.rush_down, self.current_time) and self.game_state not in ("rush", "finished") :
            self.game_state= "rush"


    def set_up_teams(self):
        self.game_start = self.current_time
        self.game_state = "fight"
        self.player_1.set_up_decks([100, 200], self.current_time, self.battle_field[0], self.player_1_field[0], "#ab6767")
        self.player_2.set_up_decks([1100, 200], self.current_time, self.battle_field[0], self.player_2_field[0], "#6668aa")


    def team_control(self, event):
        for team in (self.player_1, self.player_2):
            team.player_controller(event)


    def team_cursor_controller(self):
        for team in (self.player_1, self.player_2):
            team.current_time = self.current_time - self.game_start
            team.player_cursor_controller()

        
    def team_move(self):
        for team, velocity, opposing_units in (
            (self.player_1, [1, 0], self.player_2.field_units), 
            (self.player_2, [-1, 0], self.player_1.field_units)):

            team.generate_coins(self.current_time)
            team.move_field_units(velocity, opposing_units, self.current_time, self.game_state)


    def display_team_units(self):
        for team, deck_pos in ((self.player_1, (300, 700)), (self.player_2, (900, 700))):
            team.display_field_units(self.display, self.current_time)
            team.cursor.display_cursor(self.display)
            team.display_held_cards(self.display, deck_pos)


    def play_wimbus(self):
        run = True
        self.set_up_teams()
        self.game_start = self.current_time
        while run:
            self.clock.tick(60)
            self.change_game_state()
            self.current_time= pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if self.game_state != "finished":
                    self.team_control(event)

            if self.game_state != "finished":
                self.team_cursor_controller()
                self.team_move()

            self.display.fill("Black")
            self.display_rectangles()
            self.display_team_units()
            quick_display_text(self.display, int((self.current_time - self.game_start)/1000), "white", [600, 430])
            
            for field, team in ((self.player_1_field,self.player_1), (self.player_2_field,self.player_2)):
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

            if self.game_state == "finished":
                x, y = self.screen_size
                quick_display_text(self.display, "Finished, The winner is...", "Yellow", [x/2, y/2- 50], size= 40)
                if timer(self.show_start, self.show_winner, self.current_time):
                    quick_display_text(self.display, self.winner_text, "Yellow", [x/2, y/2+ 50], size= 40)

            pygame.display.update()


    def display_rectangles(self):
        for rect, color in [self.battle_field, self.player_1_field, self.player_2_field]:
            pygame.draw.rect(self.display, color, rect, 2)


game = Winbus()
game.play_wimbus()