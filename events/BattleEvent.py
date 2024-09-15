# BattleEvent.py

import pygame
from classes.fighter import knight,bandit1,bandit2,bandit_list

# GLOBAL VAR #
import global_var

# Define Variables

current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90

# Controls 
attackControl = False
potionControl = False
clicked = False

# Player action
def playerAttackAction():
    global current_fighter, action_cooldown

    if knight.alive:
        if current_fighter == 1:
            action_cooldown += 1

            if action_cooldown >= action_wait_time:

                if global_var.attackAction and global_var.target is not None:
                    knight.attack(global_var.target)
                    global_var.attackAction = False  #RESET
                    global_var.target = None  # RESET
                    current_fighter += 1
                    action_cooldown = 0      

# Enemy action
def enemyAttackAction() :
    global current_fighter, action_cooldown # Set Global Declaration

    # Cycle inside bandit_list
    for count, bandit in enumerate(bandit_list):
        if current_fighter == 2 + count:
            if bandit.alive :
                action_cooldown += 1
                if action_cooldown >= action_wait_time :
                    # Attack
                    bandit.attack(knight)
                    current_fighter += 1
                    action_cooldown= 0
            else:
                current_fighter += 1

# If all fighter had a turn then reset

def resetAttackActions() :
    global current_fighter, action_cooldown # Set Global Declaration

    if current_fighter > total_fighters:
        current_fighter = 1
