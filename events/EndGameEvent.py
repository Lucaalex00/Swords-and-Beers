# EndGameEvent.py

import pygame

# SETTINGS #
from settings.settings import screen,screen_height,screen_width
from settings.colors import colors
from settings.fonts import font_button

# CLASSES # 
from classes.fighter import bandit_list, knight

# GLOBAL VAR #
import global_var


# Check if the knight is dead.
def GameOverCheck():
    if not knight.alive:  # If the knight is dead, the game is over
        global_var.game_over = -1  # LOSE

# Check if all bandits are dead.
def WinCheck():

    # Count how many bandits are alive
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive:
            alive_bandits += 1
    
    global_var.alive_bandits = alive_bandits

    # If no bandits are alive, the player wins
    if global_var.alive_bandits == 0:
        global_var.game_over = 1  # WIN


#############################
#### NEW GAME MANAGEMENT ####
#############################

def draw_new_game_button():
    if global_var.game_over != 0:
        button_text = font_button.render("New Game", True, colors['white'])
        button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 70))
        pygame.draw.rect(screen, colors['black'], button_rect.inflate(20, 20))  # Background rectangle
        screen.blit(button_text, button_rect.topleft)

def check_new_game_button_click(position):
    button_rect = pygame.Rect((screen_width // 2 + 50) - 115, screen_height // 2 + 50, 130, 40)
    return button_rect.collidepoint(position)

def start_new_game():
    # RESET
    global_var.game_over = 0
    global_var.potionAction = False
    global_var.attackAction = False
    global_var.target = None
    global_var.turn_count = 1

    global_var.current_fighter = 1  # KNIGHT START
    global_var.action_cooldown = 0  # Cooldown set to 0

    # character's reset
    knight.reset()

    for bandit in bandit_list:
        bandit.reset()

                