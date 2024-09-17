# healthbar.py

import pygame
from settings.settings import screen,  screen_height, controls_panel
from settings.colors import colors
from classes.fighter import knight, bandit1, bandit2

class ManaBar():
    # Constructor
    def __init__(self, x, y, mana, max_mana):
        self.x = x
        self.y = y
        self.mana = mana
        self.max_mana = max_mana
    
    def draw_mana(self, mana):
        # Update self.mana with current mana value
        self.mana = mana

        # Calculate Mana Ratio
        ratio = self.mana / self.max_mana

        # BELOW BAR
        pygame.draw.rect(screen, colors['blue']['light'], (self.x, self.y, 90, 15))

        # ABOVE BAR
        pygame.draw.rect(screen, colors['blue']['dark'], (self.x, self.y, 90 * ratio, 15))

# Generate Bars
knight_mana_bar = ManaBar(335, screen_height - controls_panel + 70, knight.mana, knight.max_mana)

bandit1_mana_bar = ManaBar(785, screen_height - controls_panel + 70, bandit1.mana, bandit1.max_mana)

bandit2_mana_bar = ManaBar(785, screen_height - controls_panel + 120, bandit2.mana, bandit2.max_mana)





