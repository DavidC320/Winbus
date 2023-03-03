# 2/23/2023
import pygame
from unit_base import create_unit
from Game_data import cards

class Card:
    def __init__(self, name, card_type, coin_cost, unit_matrix, padding):
        self.name= name
        self.card_type= card_type
        self.coin_cost= coin_cost
        
        self.unit_matrix= unit_matrix
        self.filtered_matrix= None
        self.collision_box= None
        self.create_offsets(padding)
        
    def create_offsets(self, padding):
        # get largest unit
        get_size= lambda length: padding + length * (largest_size + padding)
        largest_width= 0
        largest_size= 0
        for row in self.unit_matrix:
            row_width =  get_size(len(row))
            if row_width > largest_width: largest_width = row_width

            for unit in row:
                temp_unit = create_unit(unit, 0)
                if temp_unit:
                    if largest_size < temp_unit.size:
                        largest_size = temp_unit.size
        
        # calculate overall size
        # overall_width = padding + largest_row * (largest_size + padding)
        overall_hight = get_size(len(self.unit_matrix))
        
        
        filtered_matrix = []
        starting_y_pos = (overall_hight/2 - (largest_size)/2 - padding) * -1
        for row in self.unit_matrix:
            filtered_row= []
            width_size = get_size(len(row))
            starting_x_pos= (width_size/2 - (largest_size)/2 - padding) * -1
            for unit in row:
                if unit:
                    filtered_unit= [unit, [starting_x_pos, starting_y_pos]]
                    print(filtered_unit)
                    filtered_row.append(filtered_unit)
                starting_x_pos += (largest_size + padding)
            filtered_matrix.append(filtered_row)
            starting_y_pos += (largest_size + padding)
            
        self.filtered_matrix = filtered_matrix
        self.collision_box = pygame.Rect(0, 0, largest_width, overall_hight)
        
def create_card(name):
    card = cards.get(name)
    if card:
        return Card(card[0], card[1], card[2], card[3], card[4])
    
