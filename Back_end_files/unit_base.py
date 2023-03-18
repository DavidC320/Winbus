# 2/20/2023
from misc_funtions import timer, use_restraint, quick_display_text
from Game_data import activators, units, attacks, conditions

import pygame
import math

def create_unit(unit_name, time):
    wanted_unit = units.get(unit_name)
    if wanted_unit:
        return Unit(wanted_unit[0], wanted_unit[1], wanted_unit[2], wanted_unit[3], wanted_unit[4],
                    wanted_unit[5], wanted_unit[6], wanted_unit[7],
                    wanted_unit[8], wanted_unit[9], wanted_unit[10], 
                    time)

def create_activator(activator_name, time):
    wanted_activator = activators.get(activator_name)
    if wanted_activator:
        return Activator(wanted_activator[0], wanted_activator[1], 
                         wanted_activator[2], wanted_activator[3], wanted_activator[4], wanted_activator[5], time)
        
def create_attack_object(attack_name):
    wanted_attack = attacks.get(attack_name)
    if not wanted_attack:
        print("Something went wrong")
        return Attack_object("Debug", "This is not supposed to be here", 
                             [], "_parent", True, [], 
                             0, 70, None, "self", 1, 2)
    
    else:
        return Attack_object(wanted_attack[0], wanted_attack[1], 
                             wanted_attack[2], wanted_attack[3], wanted_attack[4], wanted_attack[5], 
                             wanted_attack[6], wanted_attack[7], wanted_attack[8], wanted_attack[9], wanted_attack[10], wanted_attack[11])
        
def create_condition(condition_name):
    wanted_condition = conditions.get(condition_name)
    if not wanted_condition:
        print("this is not here: %s" % condition_name)
    else:
        return Condition(wanted_condition[0], wanted_condition[1])
 
def return_target_team(ally_team: list, opposing_team: list, position: list, flags: list, team_name: str, unit_object):
    "Returns the target team and if the position is past a crown"
    
    crowns = []
    opposing_crowns = []
    for enemy_unit in opposing_team:
        is_a_crown = enemy_unit.unit_type == "crown"
        opposing_crowns.append(enemy_unit)
        
        # Checks if the unit is past a crown
        p1_check= enemy_unit.position[0] < position[0] and team_name == "player 1"
        p2_check= enemy_unit.position[0] > position[0] and team_name == "player 2"
        if is_a_crown and (p1_check or p2_check):
            crowns.append(enemy_unit)
            
    # getting possible targets
    target_list= []
    if "search allies" not in flags:
        target_list.extend(opposing_team)
        
    else:
        target_list.extend(ally_team)
        target_list.extend(opposing_crowns)
        target_list.pop(target_list.index(unit_object))

    targeting_crown = bool(crowns)
    return target_list, targeting_crown
    
def return_collide_list(collide_rect: pygame.Rect, target_team: list, flags: list, unit_search_type: str, team_name: str, targeting_crown: bool, target_limit: int):
    sort_by_distance = lambda x: x[1]
    colliding_enemies = []
    position = collide_rect.center

    for enemy_unit in target_team:
        
        # Checks
        colliding = collide_rect.colliderect(enemy_unit.collision_rect)
        alive = enemy_unit.is_alive
        seen_enemy = colliding and alive

        # searches
        target_all = "all" in unit_search_type and enemy_unit.unit_type != "spell"
        is_target_unit = enemy_unit.unit_type in unit_search_type
        search_filters = (target_all or is_target_unit)

        # target filters
        target_flags = ["search injured"]
        no_target_flags = len(set(flags).intersection(target_flags)) == 0 # segment form David Alber
        # https://stackoverflow.com/questions/16138015/checking-if-any-elements-in-one-list-are-in-another
        # the intersection creates a set of items that appear in both lists

        target_injured = "search injured" in flags and enemy_unit.health < enemy_unit.max_health
        search_flags = no_target_flags or target_injured

        # override
        see_crown = enemy_unit.unit_type == "crown" and enemy_unit.team_name != team_name
        target_crown = targeting_crown and see_crown

        if seen_enemy and (search_filters and search_flags or target_crown or see_crown):
            distance = pygame.math.Vector2(position[0], position[1]).distance_to(enemy_unit.position)
            colliding_enemies.append((enemy_unit, distance))
    else:
        colliding_enemies.sort(key= sort_by_distance)
        clean_colliding_enemies= []
        for unit, _ in colliding_enemies:
            clean_colliding_enemies.append(unit)
        colliding_enemies = clean_colliding_enemies
    return colliding_enemies[:target_limit]
    

##############################################################################################################################################
#################################################################### Unit ####################################################################
##############################################################################################################################################

class Unit:
    def __init__(
            self, 
            name: str, unit_type: str, flags: list, size: int, color: str,
            health: list, walk_speed: int, attack: list,
            search_unit_type: str, search_range: int, properties: list, 
            time: int):
        # rectangles
        self.collision_rect= None
        self.search_rect= None

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
        self.attack = []
        for attack_name in attack:
            attack = create_attack_object(attack_name)
            if attack:
                self.attack.append(attack)

        # searching
        self.search_unit_type= search_unit_type
        self.search_unit_type.append("crown")
        self.search_range= search_range

        # properties
        self.properties= []
        for activator_name in properties:
            self.properties.append(create_activator(activator_name, time))

        # other info
        self.attacking = False
        self.velocity= [0, 0]
        self.target= None
        self.attack_time= 0
        self.restraint= None
        self.team_name= None
        self.action= []
        self.targeting_crown= False

        self.stored_units= []
        self.data_text = ""
        self.create_rectangles()

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
                
    #######################################################################################################################################
    ############################################################## searching ##############################################################
    def attack_target(self, current_time, ally_team, opposing_team, game_state):
        target= self.target
        if target:
            self.attacking = self.collision_rect.colliderect(target.collision_rect)
        else:
            self.attacking = False

        for attack in self.attack:
            if attack.conditions_met(game_state, self):
                attacking, actions = attack.attack_targets(current_time, ally_team, opposing_team, self.team_name, self)
                self.action.extend(actions)
                if self.attacking != True and attacking: self.attacking = True


    def search_for_target(self, opposing_team, ally_team, current_time, game_state):
        target = self.target
        target_list, self.targeting_crown = return_target_team(ally_team, opposing_team, self.position, self.flags, self.team_name, self)

        if isinstance(target, Unit):
            target_not_seen = not (self.search_rect.colliderect(target.collision_rect) or self.targeting_crown)
            target_dead = not target.is_alive
            # print("%s from %s is colliding with target: %s, target is alive: %s" % (self.name, self.team_name, target_not_seen, target_dead))
            if target_not_seen or target_dead:
                self.target= None

        else:
            seen_enemies = return_collide_list(self.search_rect, target_list, self.flags, self.search_unit_type, self.team_name, self.targeting_crown, 1)
            
            if seen_enemies:
                self.target= seen_enemies[0]
                
                self.attacking = self.collision_rect.colliderect(self.target.collision_rect)
                self.attack_time= current_time
                
        self.attack_target(current_time, ally_team, opposing_team, game_state)

    
    ############################################################## searching ##############################################################
    #######################################################################################################################################

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
        for rect in (self.collision_rect, self.search_rect):
            rect.center = self.position


    def create_rectangles(self):
        size = self.size
        search_size = self.search_range + size

        self.collision_rect= pygame.Rect(0, 0, size, size)
        self.search_rect= pygame.Rect(0, 0, search_size, search_size)
        self.set_rect_position()


    def move(self):
        self.position[0] += self.velocity[0] * self.walk_speed
        self.position[1] += self.velocity[1] * self.walk_speed
        self.position = use_restraint(self.position, self.restraint, self.collision_rect.size)
        self.set_rect_position()


    def change_velocity(self, aimed_velocity: list):
        if not isinstance(self.target, Unit):
            self.velocity= aimed_velocity
        else:
            self.velocity = self.get_target_velocity(aimed_velocity)

        self.move()


    def get_target_velocity(self, fail_safe_velocity):
        target = self.target
        target_col = target.collision_rect
        if self.attacking:
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


    def display_unit(self, display, current_time, debug = True):
        pygame.draw.rect(display, self.color, self.collision_rect)
        
        team_color = {
            "player 1" : "red",
            "player 2" : "blue"
        }
        pygame.draw.rect(display, team_color.get(self.team_name), self.collision_rect, 4)
        health_text_pos= [self.position[0], self.position[1] + 5 + self.size/2]
        quick_display_text(display, f"{self.health} \ {self.max_health}", "white",health_text_pos,size=10)
        
        if debug:
            pygame.draw.rect(display, "yellow", self.search_rect, 5)

            for attack in self.attack:
                attack.display_attack(display, current_time)

            target_text_pos= [self.position[0], self.position[1] + 15 + self.size/2]
            if isinstance(self.target, Unit):
                quick_display_text(display, self.target.name, "white", target_text_pos, size=10)
            else:
                quick_display_text(display, self.target, "white", target_text_pos, size=10)
            target_text_pos= [self.position[0], self.position[1] + 25 + self.size/2]
            quick_display_text(display, self.data_text, "white", target_text_pos, size=10)

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

class Condition:
    def __init__(self, condition_type, condition_value):
        self.condition_type = condition_type
        """
        game state
        not game state
        dead
        """
        self.condition_value = condition_value
#############################################################################################################################################
################################################################# Activator #################################################################
#############################################################################################################################################

##########
# attack
##########
                
class Attack_object:
    def __init__(
        self, name: str, description: str, 
        conditions: list, unit_target_type: str, stop_when_attack: bool, flags: list,
        damage: int, attack_range: int, blast_size: int, blast_type: str, target_limit: int, reload_time: int
        ):
        self.name = name
        self.description = description
        
        # damage controls
        self.conditions = []
        for condition_name in conditions:
            condition = create_condition(condition_name)
            if condition:
                self.conditions.append(condition)
        
        self.unit_target_type = unit_target_type
        self.stop_when_attack = stop_when_attack
        self.flags = flags
        
        # Damage
        self.damage = damage
        self.attack_range = pygame.Rect(0, 0, attack_range, attack_range)
        self.blast_size = blast_size
        self.blast_type = blast_type
        """
        blast types changes where the blast is located.
        target = the blast's center is the target
        self = the blast center is the unit itself
        """
        self.target_limit = target_limit
        self.reload_time = reload_time
        
        # Damage data
        self.target_positions = []
        self.blasts = []
        self.show_start_time= 0
        self.attack_fire_time= 0
        
        
    def conditions_met(self, game_state, unit):
        if self.unit_target_type == "_parent":
            self.unit_target_type = unit.search_unit_type
        if self.flags == "_parent":
            self.flags = unit.flags

        
        self.attack_range.center= unit.position
        
        for condition in self.conditions:
            if condition.condition_type == "game state" and condition.condition_value != game_state:
                return False
            
            elif condition.condition_type == "not game state" and condition.condition_value == game_state:
                return False

            elif condition.condition_type == "dead" and unit.is_alive:
                return False
        else:
            return True
        
        
    def display_attack(self, display, current_time):
        filtered_list = []
        filtered_blasts = []
        
        for user_position, target_position, time, length in self.target_positions:
            pygame.draw.line(display, "cyan", user_position, target_position, 5)
            if not timer(time, length - .10, current_time):
                filtered_list.append((user_position, target_position, time, length))
        
        for blast_rect, time, length in self.blasts:
            pygame.draw.rect(display, "cyan", blast_rect, 4, 1)
            if not timer(time, length - .10, current_time):
                filtered_blasts.append((blast_rect, time, length))
        
        pygame.draw.rect(display, "red", self.attack_range, 5)
        
        self.target_positions = filtered_list
        self.blasts = filtered_blasts
                
            
                
    def get_in_blast(self, target_team, blast_rect):
        caught = []
        for unit in target_team:
            if blast_rect.colliderect(unit.collision_rect):
                caught.append(unit)
        return caught
        
        
    def attack_targets(self, current_time, ally_team, enemy_team, team_name, parent_unit):
        opposing_team, _ = return_target_team(ally_team, enemy_team, self.attack_range.center, self.flags, team_name, parent_unit)
        opposing_team = return_collide_list(self.attack_range, opposing_team, self.flags, self.unit_target_type, team_name, False, self.target_limit)
        actions = []

        for target in opposing_team:

            # checks
            firerate = timer(self.attack_fire_time, self.reload_time, current_time)
            if firerate:
                actions.append("attacked")

            # flag checks
            attack_allies = "attack allies" in self.flags and target.team_name == team_name
            not_target_allies = not "attack allies" in self.flags

            if firerate and (attack_allies or not_target_allies):
                self.target_positions.append((parent_unit.position, target.position, current_time, self.reload_time))
                
                if self.blast_size:
                    
                    blast_pos = {
                        "target" : target.position,
                        "self" : parent_unit.position
                    }
                    x, y = blast_pos.get(self.blast_type)
                    blast_rect = pygame.Rect(0, 0, self.blast_size, self.blast_size)
                    blast_rect.center = (x, y)
                    
                    new_targets, _ = return_target_team(ally_team, enemy_team, (x, y), self.flags, team_name, parent_unit)
                    blast_enemies = return_collide_list(blast_rect, new_targets, self.flags, self.unit_target_type, team_name, False, 30)
                    self.blasts.append((blast_rect, current_time, self.reload_time))
                    for unit in blast_enemies:
                        self.target_positions.append(((x, y), unit.position, current_time, self.reload_time))
                        unit.change_health(-self.damage)
                        if not unit.is_alive:
                            actions.append("killed")
                
                else:
                    target.change_health(-self.damage)
                    if not target.is_alive:
                            actions.append("killed")
        if opposing_team and "attacked" in actions:
            self.attack_fire_time = current_time
            
        return self.stop_when_attack and bool(opposing_team), actions
    


##########
# attack #
##########