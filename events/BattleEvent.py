# BattleEvent.py

import pygame
import random

# SETTINGS # 
from settings.settings import screen, screen_width, screen_height, controls_panel
from settings.images import victory_img, defeat_img
from settings.colors import colors

# CLASSES #
from classes.fighter import knight,bandit_list
from classes.damagetext import DamageText,damage_text_group

# EVENTS #
from events.EndGameEvent import GameOverCheck, WinCheck

# GLOBAL VAR #
import global_var

# Define Variables

current_fighter = 1
total_fighters = len(bandit_list) + current_fighter
action_cooldown = 0
action_wait_time = 90

if global_var.game_over == 0:
    # Player action
    def playerAttackAction():
        global current_fighter, action_cooldown

        if knight.alive:
            if current_fighter == 1:
                action_cooldown += 1

                if action_cooldown >= action_wait_time:

                    # Attack
                    if global_var.attackAction and global_var.target is not None:
                        knight.attack(global_var.target)
                        global_var.attackAction = False  #RESET
                        global_var.target = None  # RESET
                        current_fighter += 1
                        action_cooldown = 0  

                    # Potion
                    if global_var.potionAction: 
                        if knight.potions > 0:
                            current_fighter += 1
                            action_cooldown = 0
                            if knight.max_hp - knight.hp > global_var.potionEffect:
                                heal_amount = global_var.potionEffect + random.randint(0, 5) 
                            else:
                                heal_amount = knight.max_hp - knight.hp

                            # Calculate the amount of healing needed
                            max_possible_heal = knight.max_hp - knight.hp
                            
                            # Apply healing but ensure it does not exceed maximum HP
                            knight.hp = min(knight.hp + min(heal_amount, max_possible_heal), knight.max_hp)

                            # POTIONS NUMBERS - 1
                            knight.potions -= 1

                            # Text appears while Healing
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), colors['green']['opaque'])
                            damage_text_group.add(damage_text)
                            
                        else:
                            knight.potions = 0
                    global_var.potionAction = False

        else :
            global_var.game_over = -1

    # Enemy action
    def enemyAttackAction():
        global current_fighter, action_cooldown # Set Global Declaration

        # Cycle through bandit_list
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:

                        # Check if healing is needed
                        if knight.strength > bandit.hp and bandit.potions > 0:
                            bandit.potions -= 1
                            current_fighter += 1
                            action_cooldown = 0

                            # Calculate the amount of healing needed
                            heal_amount = global_var.potionEffect
                            max_possible_heal = bandit.max_hp - bandit.hp
                            
                            # Apply healing but ensure it does not exceed maximum HP
                            bandit.hp = min(bandit.hp + min(heal_amount, max_possible_heal), bandit.max_hp)

                            # Text appears while Healing
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(min(heal_amount, max_possible_heal)), colors['green']['opaque'])
                            damage_text_group.add(damage_text)

                        else:
                            # Attack
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1


    # If all fighter had a turn then reset
    def resetAttackActions() :
        global current_fighter, action_cooldown # Set Global Declaration

        if current_fighter > total_fighters:
            current_fighter = 1


# Main loop check for game state
def checkGameState():

    # Check if the game is over and update the game state
    GameOverCheck()  # Check for loss condition
    WinCheck()  # Check for win condition

    # Create a new surface with the same dimensions as the screen and support for alpha transparency
    overlay = pygame.Surface((screen_width, screen_height - controls_panel), pygame.SRCALPHA)
    
    
    if global_var.game_over == 1:

        # Make sure mouse is visible
        pygame.mouse.set_visible(True)

        # Fill the overlay with a dark green color at 50% opacity
        overlay.fill((0, 100, 0, 128))  # RGB and Alpha (128 is 50% opacity)

        screen.blit(overlay, (0, 0))  # Draw the overlay on the screen

        screen.blit(victory_img, (360, 220))  # Draw the victory image on top of the overlay

    elif global_var.game_over == -1:

        # Make sure mouse is visible
        pygame.mouse.set_visible(True)

        # Fill the overlay with a dark red color at 50% opacity
        overlay.fill((139, 0, 0, 128))  # RGB and Alpha (128 is 50% opacity)

        screen.blit(overlay, (0, 0))  # Draw the overlay on the screen

        screen.blit(defeat_img, (380, 220))  # Draw the defeat image on top of the overlay

    return True  # Continue the game if no end game condition is met

        


