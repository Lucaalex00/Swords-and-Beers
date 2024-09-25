import pygame
import sys
import global_var 

# SETTINGS #
from settings.settings import screen, screen_width, screen_height, controls_panel
from settings.colors import colors
from settings.images import background_img, panel_img, sword_img
from settings.fonts import font_TNR, font_potion, font_turn_text

# CLASSES #
from classes.fighter import knight, bandit_list, bandit1, bandit2
from classes.healthbar import knight_health_bar, bandit1_health_bar, bandit2_health_bar
from classes.manabar import knight_mana_bar, bandit1_mana_bar, bandit2_mana_bar
from classes.potionbutton import potion_button, button_clicked
from classes.damagetext import damage_text_group