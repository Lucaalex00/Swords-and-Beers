# potionbutton.py

import pygame

# SETINGS #
from settings.settings import screen_height
from settings.images import potion_img

# Button Class
class PotionButton:
    def __init__(self, x, y, image, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

# Potion Button Settings
button_width = 64
button_height = 64
button_x = 65
button_y = screen_height - button_height - 80

# Create Potion Button
potion_button = PotionButton(button_x, button_y, potion_img, button_width, button_height)

button_clicked = False  # Track if the button has been clicked