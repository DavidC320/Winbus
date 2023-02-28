# 2/20/2023
from misc_funtions import timer, use_restraint, quick_display_text

import pygame
import math

class Unit:
    def __init__(
            self, name: str, unit_type: str, position: list, size: int, color: str,
            health: list, walk_speed: int, attack_speed: int, damage: int,
            search_unit_type: str, search_range: int, attack_range: int,
            properties: list):
        # rectangles
        self.collision_rect= None
        self.search_rect= None
        self.attack_rect= None

        # info
        self.name= name
        self.unit_type= unit_type
        self.position= position
        self.size= size
        self.color= color
        
        # stats
        self.health, self.max_health= health
        self.walk_speed= walk_speed
        self.attack_speed= attack_speed
        self.damage= damage

        # searching
        self.search_unit_type= search_unit_type
        self.search_range= search_range
        self.attack_range= attack_range

        # properties
        self.properties= []
        for activator_name in properties:
            self.properties.append(create_activator(activator_name))

        # other info
        self.velocity= [0, 0]
        self.target= None
        self.create_rectangles()
        self.attack_time= 0
        self.restraint= None
        self.team_name= None

    def activation(self, activator):
        for effect in activator.effects:
            stat, change = effect
            self.__dict__[stat]= change
        activator.not_used = False

    def property_activator(self, activator, game_state):
        if activator.activation_type == "game state" and activator.condition == game_state:
            self.activation(activator)
            self.create_rectangles()


    def check_properties(self, game_state):
        for activator in self.properties:
            if activator.not_used:
                self.property_activator(activator, game_state)

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

    def attack_target(self, current_time):
        target= self.target
        if isinstance(target, Unit):
            if self.attack_rect.colliderect(target.collision_rect) and timer(self.attack_time, self.attack_speed, current_time):
                target.change_health(-self.damage)
                self.attack_time= current_time

    def move(self):
        self.position[0] += self.velocity[0] * self.walk_speed
        self.position[1] += self.velocity[1] * self.walk_speed
        self.position = use_restraint(self.position, self.restraint, self.collision_rect.size)
        self.set_rect_position()

    def sort_by_distance(self, unit_chunk):
        return unit_chunk[1]

    def search_for_target(self, opposing_team, current_time):
        target = self.target

        if isinstance(target, Unit):
            target_not_seen = not self.search_rect.colliderect(target.collision_rect)
            target_dead = not target.is_alive
            # print("%s from %s is colliding with target: %s, target is alive: %s" % (self.name, self.team_name, target_not_seen, target_dead))
            if target_not_seen or target_dead:
                self.target= None

        else:
            seen_enemies = []

            for enemy_unit in opposing_team:
                colliding = self.search_rect.colliderect(enemy_unit.collision_rect)
                alive = enemy_unit.is_alive
                target_all = self.search_unit_type == "all"
                is_target_unit = enemy_unit.unit_type == self.search_unit_type

                if colliding and alive and (is_target_unit or target_all):
                    distance = pygame.math.Vector2(self.position[0], self.position[0]).distance_to(enemy_unit.position)
                    seen_enemies.append((enemy_unit, distance))
            
            if seen_enemies:
                seen_enemies.sort(key= self.sort_by_distance)
                self.target= seen_enemies[0][0]
                self.attack_time= current_time

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
    
        elif self.search_rect.colliderect(target_col):
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

    def display_unit(self, display):
        pygame.draw.rect(display, self.color, self.collision_rect)
        
        team_color = {
            "player 1" : "red",
            "player 2" : "blue"
        }
        pygame.draw.rect(display, team_color.get(self.team_name), self.collision_rect, 4)
        pygame.draw.rect(display, "yellow", self.search_rect, 5)
        pygame.draw.rect(display, "orange", self.attack_rect, 5)
        health_text_pos= [self.position[0], self.position[1] + 5 + self.size/2]
        quick_display_text(display, f"{self.health} \ {self.max_health}", "white",health_text_pos,size=10)
        """
        target_text_pos= [self.position[0], self.position[1] + 15 + self.size/2]
        if isinstance(self.target, Unit):
            quick_display_text(display, self.target.name, "white", target_text_pos, size=10)
        else:
            quick_display_text(display, self.target, "white", target_text_pos, size=10)"""

class Activator:
    def __init__(
            # General info
            self, name, desc,
            # activation
            activation_type, condition, effects,
            # settings
            destroy_on_use):
        # general information
        self.name= name
        self.description= desc

        self.activation_type= activation_type
        self.condition= condition
        self.effects= effects
        self.destroy_on_use= destroy_on_use
        self.not_used= True


def create_unit(unit_name):
    wanted_unit = units.get(unit_name)
    if wanted_unit:
        return Unit(wanted_unit[0], wanted_unit[1], wanted_unit[2], wanted_unit[3], wanted_unit[4], wanted_unit[5], wanted_unit[6], wanted_unit[7], wanted_unit[8], wanted_unit[9], wanted_unit[10], wanted_unit[11], wanted_unit[12])

def create_activator(activator_name):
    wanted_activator = activators.get(activator_name)
    if wanted_activator:
        return Activator(wanted_activator[0], wanted_activator[1], 
                         wanted_activator[2], wanted_activator[3], wanted_activator[4], wanted_activator[5])

activators= {
    "crown rage" : ("Crown rage", "When the game goes into rush mode. The crown will start moving and attack the opposing crown",
                    "game state", "rush", (["walk_speed", .2], ["search_unit_type", "noble"], ["attack_range", 40]), True)
}

#
units= {
    "crown": ("Crown", "noble", [0, 0], 200, "yellow", 
              [200, 200], 0, 2, 25,
              "all", 200, 200, ["crown rage"]),

    "dagger": ("Dagger", "unit", [0, 0], 20, "Grey",
               [4, 4], .8, 1, 2,
               "all", 200, 20, []),

    "shield": ("Shield", "unit", [0, 0], 40, "Cyan",
               [30, 30], .5, 3, 0,
               "all", 200, 50, []),

    "bow": ("Bow", "unit", [0, 0], 20, "Brown",
            [4, 4], .5, 2, 2,
            "all", 200, 150, []),
    
    "wall": ("Wall", "unit", [0, 0], 60, "Tan",
             [60, 60], 0, 1, 0,
             "all", 200, 20, []),
    
    "sword": ("Sword", "noble", [0, 0], 40, "Red",
              [20, 20], 1, 1.5, 5,
              "all", 200, 30, []),
    
    "ballista": ("Ballista", "unit", [0, 0], 40, "Purple",
                 [15, 15], 0, 2.5, 10,
                 "all", 300, 200, [])
}
