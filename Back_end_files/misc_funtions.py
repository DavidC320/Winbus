# 2/22/2023
import pygame

def timer(start_time, length_time_sec, current_time):
    return current_time - start_time >= length_time_sec * 1000

def create_text(text, color, position, mode = "center", size = 22, font = "Britannic", just_rects= False):
    font = pygame.font.SysFont(font, size)
    text = font.render(str(text), False, color)
    if mode == "center":
        text_rect = text.get_rect(center=position)
    elif mode == "midleft":
        text_rect = text.get_rect(midleft=position)
    elif mode == "midright":
        text_rect = text.get_rect(midright=position)
    elif mode == "midtop":
        text_rect = text.get_rect(midtop=position)
    elif mode == "midbottom":
        text_rect = text.get_rect(midbottom=position)
    elif mode == "topleft":
        text_rect = text.get_rect(topleft=position)

    return(text, text_rect)

def quick_display_text(display, text, color, position, mode = "center", size = 22, font = "Britannic", just_rects= False, back_ground_color= None):
        text, text_rect = create_text(text, color, position, mode, size, font, just_rects)
        if back_ground_color:
            pygame.draw.rect(display, back_ground_color, text_rect)
        display.blit(text, text_rect)
        
def use_restraint( position, rectangle, size):
    x, y = position
    width, hight = size
    width /= 2
    hight /= 2
    x_l_restraint, x_r_restraint = rectangle.left + width, rectangle.right - width
    y_u_restraint, y_d_restraint = rectangle.top + hight, rectangle.bottom - hight
    
    if x > x_r_restraint:
        x = x_r_restraint
    elif x < x_l_restraint:
        x = x_l_restraint
        
    if y > y_d_restraint:
        y = y_d_restraint
    elif y < y_u_restraint:
        y = y_u_restraint
        
    return [x, y]