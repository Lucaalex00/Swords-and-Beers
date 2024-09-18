# EndGameEvent.py

from classes.fighter import bandit_list, knight

# GLOBAL VAR #
import global_var

# Check if the knight is dead.
def GameOverCheck():
    if not knight.alive:  # If the knight is dead, the game is over
        global_var.game_over = -1  # LOSE
        print('YOU LOSE')

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
        print('YOU WIN')


        