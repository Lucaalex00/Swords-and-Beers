import pygame
import sys
import global_var 

from settings.settings import screen, screen_height, controls_panel
from settings.colors import colors
from settings.images import background_img, panel_img, sword_img
from settings.fonts import font_TNR, font_potion

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
    # Draw Rectangle area
    screen.blit(panel_img, (0, screen_height - controls_panel))
    
    # Def columns position
    name_col1 = 160
    hp_col1 = 270
    mana_col1 = 340

    name_col2 = 610
    hp_col2 = 730
    mana_col2 = 795

    # Draw text in columns position
    draw_text_bars('NAME', 'HP', 'MANA', font_TNR, colors['black'], name_col1, hp_col1, mana_col1, screen_height - controls_panel + 10)
    draw_text_bars('NAME', 'HP', 'MANA', font_TNR, colors['black'], name_col2, hp_col2, mana_col2, screen_height - controls_panel + 10)

    # Show NAME, HP, MANA -> KNIGHT
    draw_text_bars(f'{knight.name:>5}', f'{knight.hp:>2}', f'{knight.mana:>5}', font_TNR, colors['gray']['opaque'], name_col1 + 2, hp_col1 + 2, mana_col1 + 5, screen_height - controls_panel + 40)

    # FOR Cycle in bandit_list
    for distance, bandit in enumerate(bandit_list):
        # Calc Y spacing for every bandit
        y_offset = (screen_height - controls_panel) + 40 + distance * 50

        # Show NAME, HP, MANA -> BANDIT
        draw_text_bars(f'{bandit.name:>5}', f'{bandit.hp:>2}', f'{bandit.mana:>6}', font_TNR, colors['gray']['opaque'], name_col2, hp_col2, mana_col2, y_offset)

# Def draw text bars (STATS) in controls panel
def draw_text_bars(text1, text2, text3, font, text_color, x1, x2, x3, y):
    img1 = font.render(text1, True, text_color)
    img2 = font.render(text2, True, text_color)
    img3 = font.render(text3, True, text_color)
    
    screen.blit(img1, (x1, y))
    screen.blit(img2, (x2, y))
    screen.blit(img3, (x3, y))

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

    # Draw Potion Button
    if potion_button.draw(screen):
        if global_var.game_over == 0:  # Check if the game is not over
            if not button_clicked:  # Only perform action if button was not clicked recently
                global_var.potionAction = True
                button_clicked = True  # Set flag to prevent repeated action
    else:
        # Do not handle button clicks if game is over
        button_clicked = False  # Ensure button_clicked flag is reset

    # Show potions numbers
    draw_text(str(knight.potions), font_potion, colors['red']['dark'], screen, 80, screen_height - controls_panel + 25)        

    # Draw Damage Text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # Draw Skill Button
    skill_menu.draw_skill_button()
    
    # SKILL MENU EVENTS
    for event in pygame.event.get():
        # QUIT EVENT
        if event.type == pygame.QUIT:
            user_choice = confirmation_screen()
            if user_choice == "close":
                run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                user_choice = confirmation_screen()
                if user_choice == "close":
                    run = False
        # CLICK EVENT
        if event.type == pygame.MOUSEBUTTONDOWN:
            global_var.clicked = True
            global_var.click_position = pygame.mouse.get_pos()  # Save click position
        
        # Handle skill menu events
        skill_menu.handle_skill_events(event)

    if global_var.game_over == 0:
        # Fight Event Managements #
        playerAttackAction()
        enemyAttackAction()
        run = checkGameState()
        resetAttackActions()
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()

        # ATTACK INIT & SET ENEMY CLICKED
        sword_visible = False  # Flag to track sword visibility

        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos):
                if bandit.alive:
                    if not sword_visible:
                        pygame.mouse.set_visible(False)
                        screen.blit(sword_img, pos)
                        sword_visible = True
                    if global_var.clicked and global_var.click_position == pos:
                        global_var.attackAction = True
                        global_var.target = bandit_list[count]
                        global_var.clicked = False
                        global_var.click_position = None
                        break
                else:
                    if sword_visible:
                        pygame.mouse.set_visible(True)
                        sword_visible = False
        if not any(bandit.rect.collidepoint(pos) for bandit in bandit_list):
            if sword_visible:
                pygame.mouse.set_visible(True)
                sword_visible = False

    else:
        checkGameState()
        draw_new_game_button()

        # QUIT EVENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            # SKILL MENU EVENTS
            skill_menu.handle_skill_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if global_var.game_over != 0:
                    if check_new_game_button_click(pygame.mouse.get_pos()):
                        start_new_game()
                        continue

    # Display Update
    pygame.display.update()

# Close Pygame
pygame.quit()
sys.exit()

# Close Pygame
pygame.quit()
sys.exit()
