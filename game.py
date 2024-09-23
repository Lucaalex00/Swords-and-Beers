import pygame
import sys
import global_var 

from settings.settings import screen, screen_width, screen_height, controls_panel
from settings.colors import colors
from settings.images import background_img, panel_img, sword_img
from settings.fonts import font_TNR, font_potion, font_turn_text

from classes.fighter import knight, bandit_list, bandit1, bandit2
from classes.healthbar import knight_health_bar, bandit1_health_bar, bandit2_health_bar
from classes.manabar import knight_mana_bar, bandit1_mana_bar, bandit2_mana_bar
from classes.potionbutton import potion_button, button_clicked
from classes.damagetext import damage_text_group
from classes.skillmenu import SkillMenu
from events.ExitEvent import confirmation_screen, draw_text
from events.BattleEvent import playerAttackAction, enemyAttackAction, resetAttackActions, checkGameState
from events.EndGameEvent import draw_new_game_button, start_new_game, check_new_game_button_click

# FRAME RATE SET
clock = pygame.time.Clock()
fps = 60

# Init
pygame.init()
skill_menu = SkillMenu()

# Def draw background
def draw_bg():
    screen.blit(background_img, (0, 0))

# Def draw controls panel
def draw_panel():
    screen.blit(panel_img, (0, screen_height - controls_panel))
    name_col1 = 160
    hp_col1 = 270
    mana_col1 = 340

    name_col2 = 610
    hp_col2 = 730
    mana_col2 = 795

    draw_text_bars('NAME', 'HP', 'MANA', font_TNR, colors['black'], name_col1, hp_col1, mana_col1, screen_height - controls_panel + 10)
    draw_text_bars('NAME', 'HP', 'MANA', font_TNR, colors['black'], name_col2, hp_col2, mana_col2, screen_height - controls_panel + 10)

    draw_text_bars(f'{knight.name:>5}', f'{knight.hp:>2}', f'{knight.mana:>5}', font_TNR, colors['gray']['opaque'], name_col1 + 2, hp_col1 + 2, mana_col1 + 5, screen_height - controls_panel + 40)

    for distance, bandit in enumerate(bandit_list):
        y_offset = (screen_height - controls_panel) + 40 + distance * 50
        draw_text_bars(f'{bandit.name:>5}', f'{bandit.hp:>2}', f'{bandit.mana:>6}', font_TNR, colors['gray']['opaque'], name_col2, hp_col2, mana_col2, y_offset)

# Def draw text bars (STATS) in controls panel
def draw_text_bars(text1, text2, text3, font, text_color, x1, x2, x3, y):
    img1 = font.render(text1, True, text_color)
    img2 = font.render(text2, True, text_color)
    img3 = font.render(text3, True, text_color)
    
    screen.blit(img1, (x1, y))
    screen.blit(img2, (x2, y))
    screen.blit(img3, (x3, y))

# Def draw turn counts
def draw_turn_counts():
    turn_text = f"Turn : {global_var.turn_count}"
    turn_img = font_turn_text.render(turn_text, True, colors['black'])
    text_rect = turn_img.get_rect(center=(screen_width // 2, screen_height // 2 + 150))
    screen.blit(turn_img, text_rect)

# Main game Loop
run = True
game_over = False
confirmation_active = False

while run:
    clock.tick(fps)
    draw_bg()
    draw_panel()
    
    # Draw Health and Mana Bars
    knight_health_bar.draw_hp(knight.hp)
    bandit1_health_bar.draw_hp(bandit1.hp)
    bandit2_health_bar.draw_hp(bandit2.hp)
    
    knight_mana_bar.draw_mana(knight.mana)
    bandit1_mana_bar.draw_mana(bandit1.mana)
    bandit2_mana_bar.draw_mana(bandit2.mana)

    # Draw Turn Counter
    draw_turn_counts()

    # Update and draw knight and bandits
    knight.update()
    knight.draw()

    for bandit in bandit_list:
        bandit.draw()
        bandit.update()

    # Draw Potion Button
    if potion_button.draw(screen):
        if global_var.game_over == 0:
            if not button_clicked:
                global_var.potionAction = True
                button_clicked = True
    else:
        button_clicked = False

    # Show potions numbers
    draw_text(str(knight.potions), font_potion, colors['red']['opaque'], screen, 80, screen_height - controls_panel + 25)        

    # Draw Damage Text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # Draw Skill Button
    skill_menu.draw_skill_button()

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            confirmation_active = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                confirmation_active = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            skill_menu.handle_skill_events(event) 
            global_var.clicked = True
            global_var.click_position = pos
            
            # Check if "New Game" button is clicked
            if global_var.game_over != 0 and check_new_game_button_click(pos):
                start_new_game()

    if confirmation_active:
        user_choice = confirmation_screen()

        if user_choice == "close":
            run = False
            break
        elif user_choice == "cancel":
            confirmation_active = False  # Reset for next interaction

    if global_var.game_over == 0:
        playerAttackAction()
        enemyAttackAction()
        
        run = checkGameState()
        resetAttackActions()

        pos = pygame.mouse.get_pos()  # Get the current position of the mouse

        # Variable to track if the sword is currently visible
        if 'sword_visible' not in globals():
            sword_visible = False  # Initialize sword visibility once

        cursor_over_bandit = False  # Variable to track if the cursor is over any bandit

        # Loop through all bandits
        for count, bandit in enumerate(bandit_list):

            # If the mouse is hovering over a specific bandit
            if bandit.rect.collidepoint(pos):
                
                # If the bandit is alive
                if bandit.alive:
                    
                    cursor_over_bandit = True  # Set cursor over bandit as true

                    # Only hide the cursor and show the sword if not already done
                    if not sword_visible:
                        pygame.mouse.set_visible(False)  # Hide the default mouse cursor
                        sword_visible = True  # Mark the sword as visible
                    
                    # Draw the sword at the mouse position
                    screen.blit(sword_img, pos)

                    # Check for attack action
                    if global_var.clicked and global_var.click_position == pos:
                        global_var.attackAction = True  # Trigger the attack action
                        global_var.target = bandit_list[count]  # Set the target bandit
                        global_var.clicked = False  # Reset click state
                        global_var.click_position = None  # Reset click position
                        skill_menu.select_target(pos, bandit_list)  # Select target from skill menu

                        break  # Exit loop after handling click

        # If the cursor is not hovering over any bandit
        if not cursor_over_bandit:
            if sword_visible:  # If the sword is currently visible
                pygame.mouse.set_visible(True)  # Show the normal mouse cursor
                sword_visible = False  # Reset the sword visibility flag

    else:
        checkGameState()
        draw_new_game_button()

    pygame.display.update()

# Close Pygame
pygame.quit()
sys.exit()
