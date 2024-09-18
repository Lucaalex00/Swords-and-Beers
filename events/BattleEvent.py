# BattleEvent.py

import random

# SETTINGS # 
from settings.settings import screen
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
total_fighters = 3
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
    GameOverCheck() # LOSE
    WinCheck() # WIN

    if global_var.game_over == 1:
        return False # Stop game
    elif global_var.game_over == -1:
        return False # Stop game
    return True # If any condition is not TRUE, continue the game
        


