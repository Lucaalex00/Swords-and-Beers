import pygame
import sys
import time
from settings.colors import colors
from settings.settings import screen_width, screen_height, screen

pygame.font.init()
pygame.display.init()

# Font per il testo
font = pygame.font.Font(None, 36)

# Funzione per disegnare il testo
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Funzione per disegnare i pulsanti
def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            return action
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    draw_text(text, font, colors['white'], screen, x + w // 2, y + h // 2)

    return None

# Funzione per la schermata di conferma
def confirmation_screen():
    start_time = time.time() + 1
    while True:
        screen.fill(colors['black'])

        # Tempo trascorso
        elapsed_time = time.time() - start_time
        remaining_time = 3 - elapsed_time

        if remaining_time <= 1:
            return "cancel"

        # Disegna il testo di conferma e il timer
        draw_text("Sei sicuro di voler uscire?", font, colors['white'], screen, screen_width // 2, screen_height // 4)
        draw_text(f"Tempo rimasto: {int(remaining_time)}", font, colors['red']['opaque'], screen, screen_width // 2, screen_height // 2 + 70)

        # Disegna i pulsanti "Chiudi" e "Annulla"
        close_action = draw_button("Chiudi", screen_width // 2 - 120, screen_height // 2, 100, 50, colors['red']['dark'], (200, 0, 0), action="close")
        cancel_action = draw_button("Annulla", screen_width // 2 + 20, screen_height // 2, 100, 50, colors['green']['dark'], (0, 200, 0), action="cancel")

        # Gestione degli eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if close_action:
            return close_action
        if cancel_action:
            return cancel_action

        pygame.display.update()
