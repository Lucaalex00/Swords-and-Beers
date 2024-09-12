# game.py (MAIN)

import pygame
import sys
from settings.settings import screen, screen_height, screen_width, controls_panel
from settings.colors import colors
from events.ExitEvent import confirmation_screen
from classes.fighter import knight,bandit_list,bandit1,bandit2
from classes.healthbar import knight_health_bar, bandit1_health_bar, bandit2_health_bar
from classes.manabar import knight_mana_bar, bandit1_mana_bar, bandit2_mana_bar
clock= pygame.time.Clock()
fps = 60

#INIT
pygame.init()

# Definiamo i Fonts
font_TNR = pygame.font.SysFont('Times New Roman', 26)

# Carica e scala le immagini
background_img = pygame.image.load("./storage/backgrounds/background-3.png").convert_alpha()

panel_img = pygame.image.load("./storage/backgrounds/panel.png").convert_alpha()
panel_img = pygame.transform.scale(panel_img, (screen_width, controls_panel))

# Funzione per disegneare il testo delle barre della vita e del mana
def draw_text_health_bars(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# Funzione per disegnare lo sfondo
def draw_bg():
    screen.blit(background_img, (0, 0))

# Funzione per disegnare il menu
def draw_panel():
    # Disegna il pannello rettangolare
    screen.blit(panel_img, (0, screen_height - controls_panel))
    
    # Mostra le INFO dei personaggi (TITOLO)
    draw_text_health_bars(f'NAME |  HP  | MANA' , font_TNR, colors['black'], 100, screen_height - controls_panel + 10)
    draw_text_health_bars(f'NAME |  HP  | MANA' , font_TNR, colors['black'], 550, screen_height - controls_panel + 10)

    # Mostra le INFO dei personaggi (STATS)

    # Mostra il nome e la salute (PC).
    draw_text_health_bars(f'{knight.name}     {knight.hp}       {knight.mana}', font_TNR, colors['gray']['opaque'], 100, screen_height - controls_panel + 40)

    # Ciclo all'interno della mia bandit_list
    for distance, i in enumerate(bandit_list):
        # Mostra il nome e la salute (ENEMIES).
        draw_text_health_bars(f'{i.name}      {i.hp}        {i.mana}', font_TNR, colors['gray']['opaque'], 550, (screen_height - controls_panel) + 40 + distance * 50)

# Main loop del gioco
run = True
while run:

    # Imposta gli fps al valore della variabile (60)
    clock.tick(fps)

    # Disegna lo sfondo
    draw_bg()

    # Disegna il menu
    draw_panel()
    knight_health_bar.draw_hp(knight.hp)
    bandit1_health_bar.draw_hp(bandit1.hp)
    bandit2_health_bar.draw_hp(bandit2.hp)
    
    knight_mana_bar.draw_mana(knight.mana)
    bandit1_mana_bar.draw_mana(bandit1.mana)
    bandit2_mana_bar.draw_mana(bandit2.mana)

    knight.mana = 5
    # Disegna il Fighter
    knight.update()
    knight.draw()

    # Disegna i nemici    
    for bandit in bandit_list :
        bandit.draw()
        bandit.update()

    # Gestione degli eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quando l'utente preme la X, mostra la schermata di conferma
            user_choice = confirmation_screen()
            if user_choice == "close":
                run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                user_choice = confirmation_screen()
                if user_choice == "close":
                    run = False

    # Aggiornamento dello schermo
    pygame.display.update()

# Chiusura di pygame
pygame.quit()
sys.exit()
