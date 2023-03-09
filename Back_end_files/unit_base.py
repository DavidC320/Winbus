# 2/20/2023
from misc_funtions import timer, use_restraint, quick_display_text
from Game_data import activators, units, area_attacks

import pygame
import math

def create_unit(unit_name, time):
    wanted_unit = units.get(unit_name)
    if wanted_unit:
        return Unit(wanted_unit[0], wanted_unit[1], wanted_unit[2], wanted_unit[3], wanted_unit[4], wanted_unit[5], wanted_unit[6], wanted_unit[7], wanted_unit[8], wanted_unit[9], wanted_unit[10], wanted_unit[11], wanted_unit[12], time)

def create_activator(activator_name, time):
    wanted_activator = activators.get(activator_name)
    if wanted_activator:
        return Activator(wanted_activator[0], wanted_activator[1], 
                         wanted_activator[2], wanted_activator[3], wanted_activator[4], wanted_activator[5], time)

def create_area_attack(area_attack_name):
    wanted_area_attack = area_attacks.get(area_attack_name)
    if wanted_area_attack:
        return Area_attack_object(wanted_area_attack[0], wanted_area_attack[1], wanted_area_attack[2])
    else:
        return 0

##############################################################################################################################################
#################################################################### Unit ####################################################################
##############################################################################################################################################

class Unit:
    def __init__(
            self, name: str, unit_type: str, flags: list, size: int, color: str,
            health: list, walk_speed: int, attack_speed: int, damage: int,
            search_unit_type: str, search_range: int, attack_range: int,
            properties: list, time: int):
        # rectangles
        self.collision_rect= None
        self.search_rect= None
        self.attack_rect= None

        # info
        self.name= name
        self.unit_type= unit_type
        self.position= [0, 0]
        self.flags= flags
        self.size= size
        self.color= color
        
        # stats
        self.health, self.max_health= health
        self.walk_speed= walk_speed
        self.attack_speed= attack_speed
        self.damage= damage
        if isinstance(damage, str):
            self.damage = create_area_attack(damage)

        # searching
        self.search_unit_type= search_unit_type
        self.search_unit_type.append("crown")
        self.search_range= search_range
        self.attack_range= attack_range

        # properties
        self.properties= []
        for activator_name in properties:
            self.properties.append(create_activator(activator_name, time))

        # other info
        self.velocity= [0, 0]
        self.target= None
        self.create_rectangles()
        self.attack_time= 0
        self.restraint= None
        self.team_name= None
        self.action= []
        self.targeting_crown= False

        self.stored_units= []

    ########################################################################################################################################
    ############################################################## Activators ##############################################################
    def activation_effects(self, activator):
        for stat, operation, change in activator.effects:

            # Sets a variable to a different number
            if operation == "set":
                self.__dict__[stat]= change

            # Changes the variable via sum
            elif operation == "change":
                self.__dict__[stat] += change

            # Creates a summoned unit
            elif operation == "spawn":
                unit_name, offset = change
                x, y = self.position
                x_offset, y_offset = offset
                new_x, new_y = x + x_offset, y + y_offset
                self.stored_units.append((unit_name, [new_x, new_y]))

        if activator.destroy_on_use:
            activator.not_used = False

    def check_activator(self, activator, game_state, current_time):
        activation_type = activator.activation_type
        condition = activator.condition

        check_game_state = activation_type == "game state" and condition == game_state
        check_timer = activation_type == "timer" and timer(activator.start_time, condition, current_time)
        check_actions = activation_type == "check actions" and condition in self.action

        if check_game_state or check_timer or check_actions:
            print(check_game_state, check_timer, check_actions)
            activator.start_time = current_time
            self.activation_effects(activator)
            self.create_rectangles()


    def check_properties(self, game_state, current_time):
        for activator in self.properties:
            if activator.not_used:
                self.check_activator(activator, game_state, current_time)
        self.action.clear()
    ############################################################## Activators ##############################################################
    ########################################################################################################################################
                
    def check_flags(self, opposing_team, current_time):
        if "attack_area_on_death" in self.flags and isinstance(self.damage, Area_attack_object):
            self.damage.set_rect(self.position, current_time)
            blast_enemies = self.colliding_units(opposing_team, self.damage.collision_rect, self.damage.target_limit)
            for unit, _ in blast_enemies:
                unit.change_health(-self.damage.damage)


    @property
    def is_alive(self):
        return self.health > 0
    
    def change_health(self, number):
        self.health += number
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health <= 0:
            del self


    def set_rect_position(self):
        for rect in (self.collision_rect, self.search_rect, self.attack_rect):
            rect.center = self.position


    def create_rectangles(self):
        size = self.size
        search_size = self.search_range + size
        attack_size = self.attack_range + size

        self.collision_rect= pygame.Rect(0, 0, size, size)
        self.search_rect= pygame.Rect(0, 0, search_size, search_size)
        self.attack_rect= pygame.Rect(0, 0, attack_size, attack_size)
        self.set_rect_position()


    def attack_target(self, opposing_team, current_time):
        target= self.target

        if isinstance(target, Unit):

            # checks
            target_in_attack_range = self.attack_rect.colliderect(target.collision_rect)
            firerate = timer(self.attack_time, self.attack_speed, current_time)
            if target_in_attack_range and firerate:
                self.action.append("attacked")

            # flag checks
            dont_attack = not "no attack" in self.flags
            attack_allies = "attack allies" in self.flags and target.team_name == self.team_name

            if target_in_attack_range and firerate and dont_attack and attack_allies:
                if isinstance(self.damage, Area_attack_object):
                    self.damage.set_rect(target.position, current_time)
                    blast_enemies = self.colliding_units(opposing_team, self.damage.collision_rect, self.damage.target_limit)
                    for unit, _ in blast_enemies:
                        unit.change_health(-self.damage.damage)
                
                else:
                    target.change_health(-self.damage)
                self.attack_time= current_time

    def move(self):
        self.position[0] += self.velocity[0] * self.walk_speed
        self.position[1] += self.velocity[1] * self.walk_speed
        self.position = use_restraint(self.position, self.restraint, self.collision_rect.size)
        self.set_rect_position()

    def colliding_units(self, opposing_team, collide_rect, grab_limit):
        sort_by_distance = lambda x: x[1]
        colliding_enemies = []

        for enemy_unit in opposing_team:
            
            # Checks
            colliding = collide_rect.colliderect(enemy_unit.collision_rect)
            target_crown = self.targeting_crown and enemy_unit.unit_type == "crown"

            alive = enemy_unit.is_alive

            target_all = "all" in self.search_unit_type
            is_target_unit = enemy_unit.unit_type in self.search_unit_type

            if (colliding or target_crown) and alive and (is_target_unit or target_all):
                distance = pygame.math.Vector2(self.position[0], self.position[1]).distance_to(enemy_unit.position)
                colliding_enemies.append((enemy_unit, distance))
        else:
            colliding_enemies.sort(key= sort_by_distance)

        return colliding_enemies


    def search_for_target(self, opposing_team, current_time):
        target = self.target
        crowns = []
        for enemy_unit in opposing_team:
            is_a_crown = enemy_unit.unit_type == "crown"
            p1_check= enemy_unit.position[0] < self.position[0] and self.team_name == "player 1"
            p2_check= enemy_unit.position[0] > self.position[0] and self.team_name == "player 2"
            if is_a_crown and (p1_check or p2_check):
                crowns.append(enemy_unit)
        # getting possible targets
        target_list= []

        self.targeting_crown = bool(crowns)

        if isinstance(target, Unit):
            target_not_seen = not (self.search_rect.colliderect(target.collision_rect) or self.targeting_crown)
            target_dead = not target.is_alive
            # print("%s from %s is colliding with target: %s, target is alive: %s" % (self.name, self.team_name, target_not_seen, target_dead))
            if target_not_seen or target_dead:
                self.target= None

        else:
            seen_enemies = self.colliding_units(opposing_team, self.search_rect, "all")
            
            if seen_enemies:
                self.target= seen_enemies[0][0]
                self.attack_time= current_time
        self.attack_target(opposing_team, current_time)

    def change_velocity(self, aimed_velocity: list):
        if not isinstance(self.target, Unit):
            self.velocity= aimed_velocity
        else:
            self.velocity = self.get_target_velocity(aimed_velocity)

        self.move()

    def get_target_velocity(self, fail_safe_velocity):
        target = self.target
        target_col = target.collision_rect
        if self.attack_rect.colliderect(target_col):
            return [0, 0]
    
        elif self.search_rect.colliderect(target_col) or self.targeting_crown:
            # Mattineau https://stackoverflow.com/questions/20044791/how-to-make-an-enemy-follow-the-player-in-pygame
            x, y = self.position
            tx, ty = target.position
            dx, dy, = tx - x, ty - y
            distance = math.hypot(dx, dy)

            # normalize to range of 0 - 1
            dx, dy = dx / distance, dy / distance
            return [dx, dy]
        else:
            return fail_safe_velocity

    def display_unit(self, display, current_time, debug = False):
        pygame.draw.rect(display, self.color, self.collision_rect)
        
        team_color = {
            "player 1" : "red",
            "player 2" : "blue"
        }
        pygame.draw.rect(display, team_color.get(self.team_name), self.collision_rect, 4)
        health_text_pos= [self.position[0], self.position[1] + 5 + self.size/2]
        quick_display_text(display, f"{self.health} \ {self.max_health}", "white",health_text_pos,size=10)
        
        if isinstance(self.damage, Area_attack_object):
            self.damage.display_rect(display, current_time, 5)
        
        if debug:
            pygame.draw.rect(display, "yellow", self.search_rect, 5)
            pygame.draw.rect(display, "orange", self.attack_rect, 5)
            target_text_pos= [self.position[0], self.position[1] + 15 + self.size/2]
            if isinstance(self.target, Unit):
                quick_display_text(display, self.target.name, "white", target_text_pos, size=10)
            else:
                quick_display_text(display, self.target, "white", target_text_pos, size=10)

##############################################################################################################################################
#################################################################### Unit ####################################################################
##############################################################################################################################################

#############################################################################################################################################
################################################################# Activator #################################################################
#############################################################################################################################################
class Activator:
    def __init__(
            # General info
            self, name, desc,
            # activation
            activation_type, condition, effects,
            # settings
            destroy_on_use, time):
        # general information
        self.name= name
        self.description= desc

        self.activation_type= activation_type
        self.condition= condition
        
        # timer specific
        self.start_time= time
        
        self.effects= effects
        self.destroy_on_use= destroy_on_use
        self.not_used= True

#############################################################################################################################################
################################################################# Activator #################################################################
#############################################################################################################################################

##########
# attack
##########

class Area_attack_object:
    def __init__(self, damage, size, target_limit):
        self.damage= damage
        self.size= size
        self.target_limit= target_limit

        self.collision_rect = pygame.Rect(0, 0, size, size)
        self.start_time= 0
        self.show_collision= False

    def set_rect(self, position, current_time):
        self.collision_rect.center= position
        self.start_time= current_time
        self.show_collision= True
    
    def display_rect(self, display, current_time, length):
        if self.show_collision:
            pygame.draw.rect(display, "white", self.collision_rect, 4)
            if timer(self.start_time, length, current_time):
                self.show_collision= False


##########
# attack #
##########