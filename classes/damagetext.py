# damagetext.py

import pygame

pygame.init()
class DamageText(pygame.sprite.Sprite):
    # Usare SysFont per caricare un font di sistema
    font_damage_text = pygame.font.SysFont('Arial', 26)

    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.font_damage_text.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # MAX TEXT POSITIONING (Y)
        self.counter = 0
    
    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete text after 2 seconds
        self.counter += 1
        if self.counter > 45 :
            self.kill()



damage_text_group = pygame.sprite.Group()
