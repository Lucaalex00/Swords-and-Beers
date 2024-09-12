# healthbar.py

import pygame
from settings.settings import screen,  screen_height, controls_panel
from settings.colors import colors
from classes.fighter import knight, bandit1, bandit2
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
    
    def draw_hp(self, hp):
        # Update self.hp with current hp value
        self.hp = hp

        # Calculate Hp Ratio
        ratio = self.hp / self.max_hp
        
        # BELOW BAR
        pygame.draw.rect(screen, colors['red']['dark'], (self.x, self.y, 150, 20))

        # ABOVE BAR
        pygame.draw.rect(screen, colors['green']['dark'], (self.x, self.y, 150 * ratio, 20))

# Generate Bars
knight_health_bar = HealthBar(100, screen_height - controls_panel + 70, knight.hp, knight.max_hp)

bandit1_health_bar = HealthBar(550, screen_height - controls_panel + 70, bandit1.hp, bandit1.max_hp)

bandit2_health_bar = HealthBar(550, screen_height - controls_panel + 120, bandit2.hp, bandit2.max_hp)





