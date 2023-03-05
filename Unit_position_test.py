# 2/27/2023
# Unit group positioning
# The goal is to make a system where units can be placed in groups.

import pygame

class Unit_dummy:
    def __init__(self, size):
        self.pos= [0, 0]
        self.size = size
        self.rect= pygame.Rect(0, 0, size, size)

    def unit_display(self, display):
        self.rect.center= self.pos
        pygame.draw.rect(display, "White", self.rect, 3)

class Unit_container:
    def __init__(self, unit_matrix, padding= 0):
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
                if unit:
                    if largest_size < unit.size:
                        largest_size = unit.size
        
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
                    filtered_row.append(filtered_unit)
                starting_x_pos += (largest_size + padding)
            filtered_matrix.append(filtered_row)
            starting_y_pos += (largest_size + padding)
            
        self.filtered_matrix = filtered_matrix
        self.collision_box = pygame.Rect(0, 0, largest_width, overall_hight)
        
    def display_units(self, display, pos):
        self.collision_box.center= pos
        pygame.draw.rect(display, "Blue", self.collision_box, 3)
        for row in self.filtered_matrix:
            for unit, offset in row:
                if unit:
                    unit.pos = [pos[0] + offset[0], pos[1] + offset[1]]
                    unit.unit_display(display)
                
                
        



class Demo:
    def __init__(self):
        pygame.display.set_caption("Demo")
        self.screen_size= [800, 800]
        self.display= pygame.display.set_mode(self.screen_size)
        self.clock= pygame.time.Clock()
        self.card= Unit_container([
            [Unit_dummy(40), Unit_dummy(40)],
            [Unit_dummy(40), None, Unit_dummy(40)],
            [Unit_dummy(40), Unit_dummy(40)],
        ], 7
        )
        


    def play_demo(self):
        run = True
        while run:
            self.clock.tick(60)
            self.current_time= pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            self.display.fill("Black")
            pygame.draw.circle(self.display, "yellow", [400, 400], 20, 5)
            self.card.display_units(self.display, [400, 400])
            pygame.display.update()
            
demo = Demo()
demo.play_demo()