import pygame
from settings.settings import screen
class Fighter() :
    def __init__(self, x, y, name, max_hp, max_mana, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = max_mana
        self.mana = max_mana
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        img = pygame.image.load(f'classes/sprites/{self.name}/idle/0.png')
        self.image = pygame.transform.scale(img, (img.get_width()* 3, img.get_height()* 3))
        self.rect = self.image.get_rect()
        self.rect.center= (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)
# PG
knight = Fighter(250, 450,'Knight', 30, 20, 10, 3)

# ENEMIES
bandit1 = Fighter(850, 450, 'Bandit', 10, 5, 6, 1)
bandit2 = Fighter(700, 470, 'Bandit', 10, 5, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)