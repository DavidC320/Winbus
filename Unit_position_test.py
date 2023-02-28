# 2/27/2023
# Unit group positioning
# The goal is to make a system where units can be placed in groups.

import pygame

class Unit_dummy:
    def __init__(self, pos, size):
        self.pos= pos
        self.size = size
        self.rect= pygame.Rect(0, 0, size, size)

    def unit_display(self, display):
        self.rect.center= self.pos
        pygame.draw.rect(display, "White", self.rect, 3)

class Unit_container:
    def __init__(self, unit_matrix):
        self.unit_matrix= unit_matrix
        self.filtered_matrix= None

    def create_offsets(self, padding= 0):
        # get largest unit
        largest_size= 0
        largest_row= 0
        for row in self.unit_matrix:
            if len(row) > largest_row:
                largest_row = len(row)

            for unit in row:
                if largest_size < unit.size:
                    largest_size = unit.size
        
        # calculate overall size
        overall_width = padding + largest_row * (largest_size + padding)
        overall_hight = padding + len(self.unit_matrix) * (largest_size + padding)
        filtered_matrix = []
        



class Demo:
    def __init__(self):
        pygame.display.set_caption("Demo")
        self.screen_size= [800, 800]
        self.display= pygame.display.set_mode(self.screen_size)
        self.clock= pygame.time.Clock()
        


    def play_demo(self):
        run = True
        while run:
            self.clock.tick(60)
            self.change_game_state()
            self.current_time= pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.display.fill("Black")