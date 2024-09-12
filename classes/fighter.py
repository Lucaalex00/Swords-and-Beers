# fighter.py

import pygame
from settings.settings import screen
class Fighter() :

    # Constructor
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
        self.action = 0 # 0: Idle - 1: Attack - 2: Hurt - 3: Dead 
        
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


        # Idle Animations
        temp_list = []
        for i in range(8) :
            img = pygame.image.load(f'classes/sprites/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()* 3, img.get_height()* 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)  

        # Attack Animations
        temp_list = []
        for i in range(8) :
            img = pygame.image.load(f'classes/sprites/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()* 3, img.get_height()* 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)        
 
        # Hurt Animations
        temp_list = []
        for i in range(3) :
            img = pygame.image.load(f'classes/sprites/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()* 3, img.get_height()* 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)        

        # Death Animations
        temp_list = []
        for i in range(8) :
            img = pygame.image.load(f'classes/sprites/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()* 3, img.get_height()* 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)  

        # UPDATE Character image 
        self.image = self.animation_list[self.action][self.frame_index]

        # Avatar position
        self.rect = self.image.get_rect()
        self.rect.center= (x, y)

    # Draw Function
    def draw(self):
        screen.blit(self.image, self.rect)

    # Update Function
    def update(self):

        # Handle Animation
        animation_cooldown = 100
        
        # Update Image
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index+= 1

        # Repeat animation if has run out then reset to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index= 0


# Playable Characters
knight = Fighter(250, 400,'Knight', 30, 10, 10, 3)

# Enemies
bandit1 = Fighter(850, 400, 'Bandit', 10, 5, 6, 1)
bandit2 = Fighter(700, 420, 'Bandit', 10, 5, 6, 1)

# ADD to list
bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)