import pygame
import sys
from settings.settings import screen_width, screen_height, screen
from settings.colors import colors
from events.ExitEvent import confirmation_screen

pygame.init()

# Font per il testo
font = pygame.font.Font(None, 36)

# Funzione per disegnare il testo
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Main loop del gioco
run = True
while run:
    # Gestione degli eventi
    for event in pygame.event.get():

        ## CHIUDI
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
        ## /CHIUDI
        


    screen.fill(colors['gray']['dark'])
    # Aggiornamento dello schermo
    pygame.display.update()

# Chiusura di pygame
pygame.quit()
sys.exit()
