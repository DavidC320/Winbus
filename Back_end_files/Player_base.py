# 2/21/2023
from unit_base import create_unit, units
from Card_base import create_card, cards
from misc_funtions import use_restraint, timer, quick_display_text

import pygame
import random
from random import choice

class User_team:
    def __init__(self, field_rect, team_name, control_map):
        # cards
        self.held_cards= []
        self.deck= []
        self.discard_pile= []
        self.max_held_cards = 5
        self.max_deck = 10
        self.selected_card= 0

        # coins
        self.coins= 7
        self.coin_max = 10
        self.coin_generation= 2
        self.coin_gen_start= 0

        # controls
        self.control_map= control_map

        # cursor
        self.cursor = User_cursor(control_map)
        self.field_rect= field_rect

        # display
        self.field_units= []
        self.team_name= team_name

    @property
    def player_control_configuration(self):
        keys = pygame.key.get_pressed()
        controls= {
            "player_1": {
                "up" : keys[pygame.K_w],
                "down" : keys[pygame.K_s],
                "left": keys[pygame.K_a],
                "right": keys[pygame.K_d],
                "last card": pygame.K_q,
                "next card": pygame.K_e,
                "use card": pygame.K_c
                },

            "player_2": {
                "up" : keys[pygame.K_KP_8],
                "down" : keys[pygame.K_KP_5],
                "left": keys[pygame.K_KP_4],
                "right": keys[pygame.K_KP_6],
                "last card": pygame.K_KP_7,
                "next card": pygame.K_KP_9,
                "use card" : pygame.K_KP3
                }
        }
        return controls.get(self.control_map)
    
    ##########
    # checks #
    def team_dead(self):
        dead= True
        for unit in self.field_units:
            if unit.unit_type == "noble":
                dead = False
                break
        return dead

    # checks #
    #########

    ###############
    # Controllers #
    def player_cursor_controller(self):
        control = self.player_control_configuration
        self.cursor.controller(control)

    def player_controller(self, event):
        control = self.player_control_configuration

        if event.type == pygame.KEYDOWN:
            if event.key == control.get("last card") and self.held_cards:
                self.change_selected_card(-1)

            elif event.key == control.get("next card") and self.held_cards:
                self.change_selected_card(1)

            if event.key == control.get("use card") and self.held_cards:
                self.use_card()


    def use_card(self):
        current_card= self.held_cards[self.selected_card]
        if current_card.coin_cost <= self.coins:
            self.coins -= current_card.coin_cost
            self.add_unit(current_card.unit, self.cursor.position)

            self.discard_pile.append(current_card)
            self.held_cards.pop(self.selected_card)
            self.select_cards_for_hands()


    def change_selected_card(self, number):
        self.selected_card += number
        if self.selected_card >= len(self.held_cards):
            self.selected_card = 0
        elif self.selected_card < 0:
            self.selected_card = len(self.held_cards) -1
    # Controllers #
    ###############

    ##########
    # set up #
    def set_up_decks(self, crown_pos, current_time):
        for card_list in (self.deck, self.held_cards, self.discard_pile,self.field_units):
            card_list.clear()

        self.coins = 7
        self.selected_card = 0
        self.coin_gen_start= current_time

        self.add_unit("crown", crown_pos)
        self.generate_cards()
        self.select_cards_for_hands()

        """for unit_name in ["dagger", "shield", "bow"]: # debugging
            rect_place = self.cursor.restraint
            x = random.randint(rect_place.left, rect_place.right)
            y = random.randint(rect_place.top, rect_place.bottom)
            self.add_unit(unit_name, [x, y])"""
        
    
    def select_cards_for_hands(self):
        for _ in range(self.max_held_cards - len(self.held_cards)):
            if len(self.deck) == 0:
                self.deck.extend(self.discard_pile)
                self.discard_pile.clear()
            card = choice(self.deck)
            self.deck.pop(self.deck.index(card))
            self.held_cards.append(card)


    def generate_cards(self):
        card_list = list(cards.keys())
        for _ in range(self.max_deck):
            name = choice(card_list)
            self.add_card(name)


    def generate_coins(self, current_time):
        if timer(self.coin_gen_start, self.coin_generation, current_time):
            self.coins += 1
            self.coin_gen_start = current_time
            if self.coins > self.coin_max:
                self.coins = self.coin_max


    def add_card(self, card_name):
        card = create_card(card_name)
        if not card:
            print("%s does not exist." % card_name)
        else:
            self.deck.append(card)


    def add_unit(self, unit_name, position):
        unit = create_unit(unit_name)
        if not unit:
            print("%s does not exist." % unit_name)

        else:
            unit.position = position
            unit.team_name= self.team_name
            unit.restraint = self.field_rect
            self.field_units.append(unit)
    # set up #
    ##########

    ###########
    # display #
    def display_field_units(self, display):
        for unit in self.field_units:
            unit.display_unit(display)


    def display_held_cards(self, display, center_position):
        card_holder_rect = pygame.Rect(0, 0, 450, 150)
        card_holder_rect.center = center_position
        pygame.draw.rect(display, "white", card_holder_rect, 5)
        x, y = card_holder_rect.topleft
        card_width = card_holder_rect.width/self.max_held_cards
        card_hight = card_holder_rect.height
        for card in self.held_cards:
            card_rect = pygame.Rect(x, y, card_width, card_hight)

            if self.held_cards.index(card) == self.selected_card:
                pygame.draw.rect(display, "yellow", card_rect, 3)
            else:
                pygame.draw.rect(display, "blue", card_rect, 3)

            center = card_rect.center
            quick_display_text(display, card.name, "white", [center[0], center[1] - 40])
            quick_display_text(display, card.coin_cost, "white", [center[0], center[1]])
            x += card_width
    # display #
    ###########

    def move_field_units(self, velocity, opposing_team, current_time, game_state):
        for unit in self.field_units:
            if unit.is_alive: # if their alive
                unit.check_properties(game_state)
                unit.search_for_target(opposing_team, current_time)
                unit.change_velocity(velocity)
                unit.attack_target(current_time)
                unit.move()

            else: # if their dead
                self.field_units.pop(self.field_units.index(unit))


############################################################################################################################################
################################################################## Cursor ##################################################################
############################################################################################################################################

class User_cursor:
    def __init__(self, control_map):
        self.position= [0, 0]
        self.collision_rect= pygame.Rect(0, 0, 60, 60)
        self.velocity= [0, 0]
        self.speed= 5
        self.control_map= control_map
        self.color= "green"
        self.restraint = None

    ##############
    # controller #
    def controller(self, controller_configuration):
        control = controller_configuration
        
        if control.get("up") and control.get("down"):
            self.velocity[1] = 0
        elif control.get("up"):
            self.velocity[1] = -1
        elif control.get("down"):
            self.velocity[1] = 1
        else:
            self.velocity[1] = 0
            
        if control.get("left") and control.get("right"):
            self.velocity[0] = 0
        elif control.get("left"):
            self.velocity[0] = -1
        elif control.get("right"):
            self.velocity[0] = 1
        else:
            self.velocity[0] = 0
        self.move_cursor()
        
    # controller #
    ##############

    def display_cursor(self, display):
        self.collision_rect.center= self.position
        pygame.draw.rect(display, self.color, self.collision_rect, 6)
        
    def set_up(self, position, color, restraint):
        self.position= position
        self.collision_rect.center= position
        self.color= color
        self.restraint= restraint
        
    def move_cursor(self):
        x, y = self.position
        vx, vy = self.velocity
        speed = self.speed
        x += speed * vx
        y += speed * vy
        
        self.position = use_restraint([x, y], self.restraint, self.collision_rect.size)