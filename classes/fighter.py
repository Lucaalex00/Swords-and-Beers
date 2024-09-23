# fighter.py

import pygame
import random
from settings.settings import screen
from settings.colors import colors

from classes.damagetext import DamageText, damage_text_group

class Fighter() :

    # Constructor
    def __init__(self, x, y, name, max_hp, max_mana, strength, potions, is_enemy):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = max_mana
        self.mana = max_mana
        self.strength = strength
        self.start_strength = strength  # START STRENGTH VALUE
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.action = 0 # 0: Idle - 1: Attack - 2: Hurt - 3: Dead 
        self.is_enemy = is_enemy

        # POSITIONING
        self.start_x = x
        self.start_y = y
        
        # Animation & Frame Rate
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
        for i in range(10) :
            img = pygame.image.load(f'classes/sprites/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()* 3, img.get_height()* 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)  

        # UPDATE Character image 
        self.image = self.animation_list[self.action][self.frame_index]

        # Avatar position
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        print(f'{name} rect: {self.rect}')  # Verifica la posizione e dimensione del rettangolo

    # Draw Function
    def draw(self):
        screen.blit(self.image, self.rect)

    # Update Function
    def update(self):

        # Handle Animation
        animation_cooldown = 100 # ms
        
        # Update Image
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
        # Check died and keep last frame 
            if self.action == 3:  # DEATH
                self.frame_index = len(self.animation_list[self.action]) - 1 
        # Or keep idle animation
            else:
                self.idle() 
    
    # Reset Function
    def reset(self):
        self.hp = self.max_hp
        self.mana = self.max_mana
        self.potions = self.start_potions
        self.strength = self.start_strength
        self.alive = True
        self.action = 0  # IDLE
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Reset the position
        self.rect.center = (self.start_x, self.start_y)

    def idle(self) : 
        self.action = 0 # IDLE
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self) :
        self.action = 2 # HURT
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks() 

    def died(self) :
        self.action = 3 # DEATH
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks() 

    # Attack Function
        
    def attack(self, target):
        if target.alive and self.alive:

            # Verifica se il combattente è un nemico e ha abbastanza mana per la Frenzy Attack
            if self.is_enemy and self.mana >= 5:
                # Frenzy Attack
                print(f"{self.name} uses Frenzy Attack!")
                damage = round((self.strength * self.mana) / 2)  # Frenzy infligge danno in base alla forza e mana
                self.mana = 0  # Consuma tutto il mana del bandit

            else:
                # Normale attacco
                print(f"{self.name} attacks normally!")
                randRange = random.randint(-5, 5)
                damage = self.strength + randRange

            # Animazione dell'attacco
            self.action = 1  # Setta lo stato ad "Attack"
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

            # Infliggi il danno
            target.hp -= damage
            damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), colors['red']['opaque'])
            damage_text_group.add(damage_text)

            # Controlla se il bersaglio è morto
            if target.hp < 1:
                target.hp = 0
                target.alive = False
                target.died()

            # Mostra che il bersaglio è stato colpito
            target.hurt()

            # Resetta l'indice dell'animazione e il timer
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

            return damage  # Restituisci il danno inflitto
        return 0

    def mana_update(self):
        if self.is_enemy == True:
            mana_recupero = 3
            self.mana += mana_recupero
        else:
            mana_recupero = round(self.max_mana * 0.10)
            self.mana += mana_recupero
        if self.mana > self.max_mana:
            self.mana = self.max_mana

# Playable Characters
knight = Fighter(250, 400,'Knight', 50, 30, 10, 5, is_enemy = False)

# Enemies
bandit1 = Fighter(850, 400, 'Bandit', 35, 5, 6, 1, is_enemy = True)
bandit2 = Fighter(700, 420, 'Bandit', 45, 5, 8, 2, is_enemy = True)

# ADD to list
bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)