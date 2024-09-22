import pygame
import sys
import time
from settings.colors import colors
from settings.settings import screen_width, screen_height, screen

pygame.font.init()
pygame.display.init()

# Font
font = pygame.font.Font(None, 36)

# Def draw_text
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

    # Make sure mouse is visible
    pygame.mouse.set_visible(True)
    
    while True:
        # Creare una superficie con canale alfa per lo sfondo trasparente
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((10, 0, 0, 180))  # Nero con trasparenza (valore alfa: 180)

        # Fill main screen
        screen.fill((0, 0, 0))

        # Draw overlay with opacity above screen
        screen.blit(overlay, (0, 0))

        # TIME
        elapsed_time = time.time() - start_time
        remaining_time = 3 - elapsed_time  # Timer 3 seconds

        if remaining_time <= 1:
            return "cancel"

        # Draw Text & Timer
        draw_text("Are you sure to leave?", font, colors['white'], screen, screen_width // 2, screen_height // 4)
        draw_text(f"Remaining Time: {int(remaining_time)}", font, colors['red']['dark'], screen, screen_width // 2, screen_height // 2 + 70)

        # Draw Buttons "Close" and "Cancel"
        close_action = draw_button("Leave", screen_width // 2 - 150, screen_height // 2, 100, 50, colors['red']['dark'], (200, 0, 0), action="close")
        
        cancel_action = draw_button("Cancel", screen_width // 2 + 50, screen_height // 2, 100, 50, colors['green']['dark'], (0, 200, 0), action="cancel")

        # Events Management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if close_action:
            return close_action
        if cancel_action:
            return cancel_action

        pygame.display.update()

