import pygame
import sys
import global_var 

from settings.settings import screen, screen_height, screen_width, controls_panel
from settings.colors import colors
from settings.images import background_img, panel_img, sword_img

from classes.fighter import knight, bandit_list, bandit1, bandit2
from classes.healthbar import knight_health_bar, bandit1_health_bar, bandit2_health_bar
from classes.manabar import knight_mana_bar, bandit1_mana_bar, bandit2_mana_bar
from classes.potionbutton import potion_button, button_clicked
from classes.damagetext import damage_text_group

from events.ExitEvent import confirmation_screen, draw_text
from events.BattleEvent import playerAttackAction, enemyAttackAction, resetAttackActions

# FRAME RATE SET
clock = pygame.time.Clock()
fps = 60

# Init Pygame
pygame.init()

# Fonts
font_TNR = pygame.font.SysFont('Times New Roman', 26)
font_potion = pygame.font.SysFont('Sans Serif', 18)

def draw_text_bars(text1, text2, text3, font, text_color, x1, x2, x3, y):
    img1 = font.render(text1, True, text_color)
    img2 = font.render(text2, True, text_color)
    img3 = font.render(text3, True, text_color)
    
    screen.blit(img1, (x1, y))
    screen.blit(img2, (x2, y))
    screen.blit(img3, (x3, y))


# Def draw background
def draw_bg():
    screen.blit(background_img, (0, 0))

# Def draw controls panel
def draw_panel():
    # Draw Rectangle area
    screen.blit(panel_img, (0, screen_height - controls_panel))
    
    # Definisci le posizioni delle colonne
    name_col1 = 160
    hp_col1 = 270
    mana_col1 = 340

    name_col2 = 610
    hp_col2 = 730
    mana_col2 = 795

    # Intestazioni con posizioni fisse
    draw_text_bars('NAME', 'HP', 'MANA', font_TNR, colors['black'], name_col1, hp_col1, mana_col1, screen_height - controls_panel + 10)
    draw_text_bars('NAME', 'HP', 'MANA', font_TNR, colors['black'], name_col2, hp_col2, mana_col2, screen_height - controls_panel + 10)

    # Mostra Nome, HP e Mana per il giocatore
    draw_text_bars(f'{knight.name:>5}', f'{knight.hp:>2}', f'{knight.mana:>5}', font_TNR, colors['gray']['opaque'], name_col1 + 2, hp_col1 + 2, mana_col1 + 5, screen_height - controls_panel + 40)

    # Cicla attraverso i banditi
    for distance, bandit in enumerate(bandit_list):
        # Calcola la posizione Y per ciascun bandito
        y_offset = (screen_height - controls_panel) + 40 + distance * 50
        draw_text_bars(f'{bandit.name:>5}', f'{bandit.hp:>2}', f'{bandit.mana:>6}', font_TNR, colors['gray']['opaque'], name_col2, hp_col2, mana_col2, y_offset)


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
    for bandit in bandit_list:
        bandit.draw()
        bandit.update()

    # Fight Event Managements #

    # Player Turn
    playerAttackAction()

    # Enemies Turn
    enemyAttackAction()

    # Reset Fight
    resetAttackActions()

    # Reset Action Variables #

    # Make sure mouse is visible
    pygame.mouse.set_visible(True)

    # Keep mouse Position
    pos = pygame.mouse.get_pos()

   # ATTACK INIT & SET ENEMY CLICKED
    # Set initial cursor visibility
    pygame.mouse.set_visible(True)
    sword_visible = False  # Flag to track sword visibility

    # ATTACK INIT & SET ENEMY CLICKED
    for count, bandit in enumerate(bandit_list):
        # bandit area & mouse cursor collides
        if bandit.rect.collidepoint(pos):
            if bandit.alive:
                # Show the sword if the cursor is over a live enemy
                if not sword_visible:
                    pygame.mouse.set_visible(False)
                    screen.blit(sword_img, pos)
                    sword_visible = True  # Set flag to indicate sword is visible
                # Check if mouse is clicked and click position matches current position
                if global_var.clicked and global_var.click_position == pos:
                    global_var.attackAction = True  # AttackAction = True
                    global_var.target = bandit_list[count]  # Target = Clicked enemy
                    global_var.clicked = False  # RESET
                    global_var.click_position = None  # Reset click position after attack
                    break  # Exit loop after handling the click to prevent multiple processing
            else:
                # Hide sword if the enemy is no longer alive
                if sword_visible:
                    pygame.mouse.set_visible(True)
                    sword_visible = False  # Reset sword visibility flag

    # Reset sword visibility if no enemy is under the cursor
    if not any(bandit.rect.collidepoint(pos) for bandit in bandit_list):
        if sword_visible:
            pygame.mouse.set_visible(True)
            sword_visible = False


    # Draw Potion Button
    if potion_button.draw(screen):
        if not button_clicked:  # Only perform action if button was not clicked recently
            global_var.potionAction = True
            button_clicked = True  # Set flag to prevent repeated action

            # Show potions numbers

    else:
        draw_text(str(knight.potions), font_potion, colors['red']['dark'], screen, 80, screen_height - controls_panel + 25)
        button_clicked = False  # Reset flag when button is not clicked

    # Draw Damage Text
    damage_text_group.update()
    damage_text_group.draw(screen)

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
            global_var.click_position = pygame.mouse.get_pos()  # Save click position

    # Display Update
    pygame.display.update()

# Close Pygame
pygame.quit()
sys.exit()
