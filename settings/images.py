# images.py

import pygame
from settings.settings import screen_width,controls_panel

# Load and scale Images

# BACKGROUND 
background_img = pygame.image.load("./storage/backgrounds/background-3.png").convert_alpha()

# PANEL CONTROLS
panel_img = pygame.image.load("./storage/backgrounds/panel.png").convert_alpha()
panel_img = pygame.transform.scale(panel_img, (screen_width, controls_panel))

# SWORD CURSOR
sword_img = pygame.image.load("./storage/icons/sword.png").convert_alpha()
