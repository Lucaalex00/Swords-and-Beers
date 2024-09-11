import pygame
import sys
from settings.settings import screen, screen_height, screen_width
from settings.colors import colors
from events.ExitEvent import confirmation_screen
from classes.fighter import knight,bandit_list
clock= pygame.time.Clock()
fps = 60
pygame.init()

# Font per il testo
font = pygame.font.Font(None, 36)

# Funzione per disegnare il testo
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Carica e scala le immagini
background_img = pygame.image.load("./storage/media/background-3.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Funzione per disegnare lo sfondo
def draw_bg():
    screen.blit(background_img, (0, 0))


# Main loop del gioco
run = True
while run:

    # Imposta gli fps al valore della variabile (60)
    clock.tick(fps)

    # Disegna lo sfondo
    draw_bg()

    # Disegna il Fighter
    knight.draw()

    # Disegna i nemici    
    for bandit in bandit_list :
        bandit.draw()

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
