# 2/21/2023
from unit_base import create_unit
from Card_base import create_card
from Game_data import cards
from misc_funtions import use_restraint, timer, quick_display_text

import pygame
from random import choice

class User_team:
    def __init__(self, team_name, control_map):
        # cards
        self.crown= "crown"

        self.init_deck = []

        self.held_cards= []
        self.deck= []
        self.discard_pile= []
        self.max_held_cards = 5
        self.max_deck = 10
        self.selected_card= 0
        
        # time
        self.current_time = 0

        # coins
        self.coins= 10
        self.coin_max = 10
        self.coin_generation= 2
        self.coin_gen_start= 0

        # controls
        self.control_map= control_map

        # cursor
        self.cursor = User_cursor()
        self.field_rect= None

        # display
        self.field_units= []
        self.team_name= team_name

    @property
    def player_control_configuration(self):
        controls= {
            "player_1": {
                "up" : pygame.K_w,
                "down" : pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d,
                "last card": pygame.K_q,
                "next card": pygame.K_e,
                "use card": pygame.K_c
                },

            "player_2": {
                "up" : pygame.K_KP_8,
                "down" : pygame.K_KP_5,
                "left": pygame.K_KP_4,
                "right": pygame.K_KP_6,
                "last card": pygame.K_KP_7,
                "next card": pygame.K_KP_9,
                "use card" : pygame.K_KP1
                }
        }
        controls_map= {
            "player_1": {
                "up" : "W",
                "down" : "S",
                "left": "A",
                "right": "D",
                "last card": "Q",
                "next card": "E",
                "use card": "C"
                },

            "player_2": {
                "up" : "8",
                "down" : "5",
                "left": "4",
                "right": "6",
                "last card": "7",
                "next card": "9",
                "use card" : "1"
                }
        }
        return controls.get(self.control_map), controls_map.get(self.control_map)
    
    ##########
    # checks #
    def team_dead(self):
        dead= True
        for unit in self.field_units:
            if unit.unit_type in ["noble", "crown"]:
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
        control = self.player_control_configuration[0]

        if event.type == pygame.KEYDOWN:
            if event.key == control.get("last card") and self.held_cards:
                self.change_selected_card(-1)

            elif event.key == control.get("next card") and self.held_cards:
                self.change_selected_card(1)

            if event.key == control.get("use card") and self.held_cards:
                self.use_card(self.held_cards[self.selected_card], self.cursor.position)


    def use_card(self, current_card, pos, add_to_deck= True):
        not_colliding_with_units = True
        for unit in self.field_units:
            if self.cursor.collision_rect.colliderect(unit.collision_rect):
                not_colliding_with_units = False
                break
            
        
        if current_card.coin_cost <= self.coins and not_colliding_with_units:
            self.coins -= current_card.coin_cost
            for row in current_card.filtered_matrix:
                for unit, offset in row:
                    new_pos = [pos[0] + offset[0], pos[1] + offset[1]]
                    self.add_unit(unit, new_pos)

            if add_to_deck:
                self.discard_pile.append(current_card)
                self.held_cards.pop(self.selected_card)
                self.select_cards_for_hands()


    def change_selected_card(self, number):
        self.selected_card += number
        if self.selected_card >= len(self.held_cards):
            self.selected_card = 0
        elif self.selected_card < 0:
            self.selected_card = len(self.held_cards) -1
            
        self.change_cursor_size()
    # Controllers #
    ###############

    ##########
    # set up #
    def change_cursor_size(self):
        card = self.held_cards[self.selected_card]
        if not card:
            print("couldn't get size")
            self.cursor.change_size((60, 60))
        else:
            print("got size")
            self.cursor.change_size(card.collision_box.size)
    
    def set_up_decks(self, crown_pos, current_time, field_rect, cursor_rect, cursor_color):
        self.field_rect = field_rect
        self.field_units.clear()
        self.held_cards.clear()
        self.deck.clear()
        self.discard_pile.clear()

        self.coins = 10
        self.selected_card = 0
        self.coin_gen_start= current_time

        crown_card = create_card(self.crown, "card crowns")
        self.use_card(crown_card, crown_pos, False)
        
        self.cursor.set_up(crown_pos, cursor_color, cursor_rect)
        
        self.generate_cards()
        self.select_cards_for_hands()
        self.change_cursor_size()
        
    
    def select_cards_for_hands(self):
        for _ in range(self.max_held_cards - len(self.held_cards)):
            if len(self.deck) == 0:
                self.deck.extend(self.discard_pile)
                self.discard_pile.clear()
            card = choice(self.deck)
            self.deck.pop(self.deck.index(card))
            self.held_cards.append(card)


    def generate_cards(self):
        card_list = list(cards.get("card units").keys())
        missing_cards = self.max_deck - len(self.init_deck)
        for card_name in self.init_deck:
            self.add_card(card_name)
        for _ in range(missing_cards):
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
        unit = create_unit(unit_name, self.current_time)
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
    def display_field_units(self, display, current_time):
        for unit in self.field_units:
            unit.display_unit(display, current_time)


    def display_held_cards(self, display, center_position):
        control_map = self.player_control_configuration[1]
        card_holder_rect = pygame.Rect(0, 0, 450, 150)
        card_holder_rect.center = center_position
        pygame.draw.rect(display, "white", card_holder_rect, 5)
        quick_display_text(display, control_map.get("last card"), "white", card_holder_rect.midleft, "midright", back_ground_color= "black")
        quick_display_text(display, control_map.get("next card"), "white", card_holder_rect.midright, "midleft", back_ground_color= "black")
        quick_display_text(display, "%s: Use card" % control_map.get("use card"), "white", card_holder_rect.midtop, "midbottom", back_ground_color= "black")


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
            unit.check_properties(game_state, current_time)
            unit.search_for_target(opposing_team, current_time)
            unit.change_velocity(velocity)

            for unit_name, position in unit.stored_units:
                self.add_unit(unit_name, position)
            unit.stored_units.clear()

    def check_field_units(self, opposing_team, current_time):
        for unit in self.field_units:
            if not unit.is_alive:
                unit.check_flags(opposing_team, current_time)
                self.field_units.pop(self.field_units.index(unit))

############################################################################################################################################
################################################################## Cursor ##################################################################
############################################################################################################################################

class User_cursor:
    def __init__(self):
        self.position= [0, 0]
        self.collision_rect= pygame.Rect(0, 0, 60, 60)
        self.velocity= [0, 0]
        self.control_map= None
        self.speed= 5
        self.color= "green"
        self.restraint = None

    ##############
    # controller #
    def controller(self, controller_configuration):
        control, self.control_map = controller_configuration
        keys = pygame.key.get_pressed()
        
        if keys[control.get("up")] and keys[control.get("down")]:
            self.velocity[1] = 0
        elif keys[control.get("up")]:
            self.velocity[1] = -1
        elif keys[control.get("down")]:
            self.velocity[1] = 1
        else:
            self.velocity[1] = 0
            
        if keys[control.get("left")] and keys[control.get("right")]:
            self.velocity[0] = 0
        elif keys[control.get("left")]:
            self.velocity[0] = -1
        elif keys[control.get("right")]:
            self.velocity[0] = 1
        else:
            self.velocity[0] = 0
        self.move_cursor()
        
    # controller #
    ##############
    
    def change_size(self, size):
        x, y = self.position
        width, height= size
        self.collision_rect = pygame.Rect(x, y, width+6, height+6)

    def display_cursor(self, display):
        self.collision_rect.center= self.position
        pygame.draw.rect(display, self.color, self.collision_rect, 6)

        if self.control_map:
            quick_display_text(display, self.control_map.get("left"), "white", self.collision_rect.midleft, "midright", back_ground_color= "black")
            quick_display_text(display, self.control_map.get("right"), "white", self.collision_rect.midright, "midleft", back_ground_color= "black")
            quick_display_text(display, self.control_map.get("up"), "white", self.collision_rect.midtop, "midbottom", back_ground_color= "black")
            quick_display_text(display, self.control_map.get("down"), "white", self.collision_rect.midbottom, "midtop", back_ground_color= "black")
        
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