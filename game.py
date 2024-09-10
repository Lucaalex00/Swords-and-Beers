import pygame

pygame.init()


# Creates the game window with the specified screen width and height.
screen_width = 800
screen_height = 400

# pygame.display.set_mode() returns a Surface object where all game elements will be drawn.
screen = pygame.display.set_mode((screen_width, screen_height))

# Sets the caption of the game window to 'Battle'. 
# This text will appear in the window's title bar.
pygame.display.set_caption('Battle')


