# game.py (MAIN)

# IMPORTS #
import pygame
import sys

# GLOBAL VAR #
import global_var 

# SETTINGS #
from settings.settings import screen, screen_height, screen_width, controls_panel
from settings.colors import colors
from settings.images import background_img, panel_img, sword_img

# CLASSES #
from classes.fighter import knight,bandit_list,bandit1,bandit2
from classes.healthbar import knight_health_bar, bandit1_health_bar, bandit2_health_bar
from classes.manabar import knight_mana_bar, bandit1_mana_bar, bandit2_mana_bar

# EVENTS #
from events.ExitEvent import confirmation_screen
from events.BattleEvent import playerAttackAction, enemyAttackAction,resetAttackActions

# FRAME RATE SET
clock= pygame.time.Clock()
fps = 60

# Init Pygame
pygame.init()

# Fonts
font_TNR = pygame.font.SysFont('Times New Roman', 26)

# Def draw health/mana bar
def draw_text_bars(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# Def draw background
def draw_bg():
    screen.blit(background_img, (0, 0))

# Def draw controls panel
def draw_panel():
    # Draw Rectangle area
    screen.blit(panel_img, (0, screen_height - controls_panel))
    
    # Show info (STATS TITLES)
    draw_text_bars(f'NAME |  HP  | MANA' , font_TNR, colors['black'], 100, screen_height - controls_panel + 10)
    draw_text_bars(f'NAME |  HP  | MANA' , font_TNR, colors['black'], 550, screen_height - controls_panel + 10)

    # Show Name & Hp / Mana (PC).
    draw_text_bars(f'{knight.name}     {knight.hp}       {knight.mana}', font_TNR, colors['gray']['opaque'], 100, screen_height - controls_panel + 40)

    # Cycle bandit_list
    for distance, i in enumerate(bandit_list):
        # Show Name & Hp / Mana (ENEMIES).
        draw_text_bars(f'{i.name}      {i.hp}        {i.mana}', font_TNR, colors['gray']['opaque'], 550, (screen_height - controls_panel) + 40 + distance * 50)


# Main game Loop
run = True
while run:

    # Set FPS (60)
    clock.tick(fps)

    # Draw Background
    draw_bg()

    # Draw Menu
    draw_panel()
    knight_health_bar.draw_hp(knight.hp)
    bandit1_health_bar.draw_hp(bandit1.hp)
    bandit2_health_bar.draw_hp(bandit2.hp)
    
    knight_mana_bar.draw_mana(knight.mana)
    bandit1_mana_bar.draw_mana(bandit1.mana)
    bandit2_mana_bar.draw_mana(bandit2.mana)

    # Draw Fighter
    knight.update()
    knight.draw()

    # Draw Enemies  
    for bandit in bandit_list :
        bandit.draw()
        bandit.update()

    # Events Management

    # Fight Event Management

        # Player Turn
        playerAttackAction()

        # Enemies Turn
        enemyAttackAction()
        
        # Reset Fight
        resetAttackActions()

    # Reset Action Variables
        
        # Make sure mouse is visible
        pygame.mouse.set_visible(True)

        # Keep mouse Position
        pos = pygame.mouse.get_pos()

        # ATTACK INIT & SET ENEMY CLICKED
    for count, bandit in enumerate(bandit_list):

        # bandit area & mouse cursor collides
        if bandit.rect.collidepoint(pos):

            # Hide Cursor and Show Sword
            pygame.mouse.set_visible(False)
            screen.blit(sword_img, pos)

            # Check if mouse is clicked
            if global_var.clicked:  
                global_var.attackAction = True  # AttackAction = True

                global_var.target = bandit_list[count]  # Target = Clicked enemy

                global_var.clicked = False  # RESET

    for event in pygame.event.get():

        # QUIT EVENT
        if event.type == pygame.QUIT:

            # When user click "X", show ExitEvent Display
            user_choice = confirmation_screen()
            if user_choice == "close":
                run = False

        elif event.type == pygame.KEYDOWN:
            # When user press "ESC", Show ExitEvent Display
            if event.key == pygame.K_ESCAPE:
                user_choice = confirmation_screen()
                if user_choice == "close":
                    run = False
        
        # CLICK EVENT
        if event.type == pygame.MOUSEBUTTONDOWN:
            global_var.clicked = True

    # Display Update
    pygame.display.update()

# Close Pygame
pygame.quit()
sys.exit()
