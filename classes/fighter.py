# fighter.py

import pygame
import random

# SETTINGS # 
from settings.settings import screen
from settings.colors import colors
from settings.fonts import font_TNR

# CLASSES #
from classes.damagetext import DamageText, damage_text_group
from classes.skilltext import SkillText

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
        

    # Draw Function
    def draw(self):
        screen.blit(self.image, self.rect)

    # Update Function
    def update(self):
        # Handle Animation
        animation_cooldown = 100  # ms

        # Update Image
        self.image = self.animation_list[self.action][self.frame_index]
        
        # Log stato corrente
        print(f"Azione corrente: {self.action}")

        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            # Death Animation (check if the character is dead and trigger death animation)
            if self.action == 3:  # Se l'azione è DEATH
                if self.frame_index >= len(self.animation_list[self.action]):
                    print(f"Personaggio {self.name} morto, blocco l'animazione sull'ultimo frame.")
                    self.frame_index = len(self.animation_list[self.action]) - 1  # Rimani sull'ultima immagine
            else:
                # Handle other animations
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.idle()  # Torna a idle solo se non è morto
                    self.frame_index = 0  # Reset dell'indice per idle
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

    # Actions Function
    def idle(self) : 
        self.action = 0 # IDLE
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self) :
        self.action = 2 # HURT
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks() 

    def died(self):
        if self.alive:  # Controlla se è vivo prima di eseguire
            self.action = 3  # Imposta l'azione a DEATH
            self.frame_index = 0  # Inizia dall'inizio dell'animazione di morte
            self.update_time = pygame.time.get_ticks()
            self.alive = False  # Imposta alive a False         

    # Attack Function
    def attack(self, target):
        if target.alive and self.alive:

            ### FRENZY SLASH (IA) ###

            # Check if the self is an enemy and is mana is equal or greater than 5
            if self.is_enemy and self.mana >= 5:

                # Frenzy Attack
                damage = round((self.strength * self.mana) / 2)  # Frenzy inflicts damage with a calc with strength and mana values.   
                self.mana = 0  # Consume all mana when use this skill

                # Enemies skill name appears on screen when used
                skill_text = SkillText(self.rect.centerx, self.rect.y - 50, "Frenzy Slash", font_TNR, colors['yellow']['dark'])
                damage_text_group.add(skill_text)

            else:

                # Normal Attack
                randRange = random.randint(-5, 5)
                damage = round(self.strength + randRange)

            # Attack animation
            self.action = 1  # ATTACK
            self.frame_index = 0    
            self.update_time = pygame.time.get_ticks()

            # Inflicts damage
            target.hp -= damage
            damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), colors['red']['opaque'])
            damage_text_group.add(damage_text)

            # Check if target is DEAD
            if target.hp < 1:
                target.hp = 0
                target.died()  # Assicurati che questa chiamata venga effettuata
                print(f"{target.name} è stato ucciso.")
                return
            # Show Target's hurt animation 
            target.hurt()

            # Reset Index animation and Timer
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

            return damage  
        return 0

    # Mana Recharge Function
    def mana_update(self):

        # RECHARGE EVERY TURN MANA
        if self.is_enemy == True:
            mana_recupero = 2
            self.mana += mana_recupero
        else:
            mana_recupero = round(self.max_mana * 0.20)
            self.mana += mana_recupero
        if self.mana > self.max_mana:
            self.mana = self.max_mana

# Playable Characters
knight = Fighter(250, 400,'Knight', 65, 30, 33, 5, is_enemy = False)

# Enemies
bandit1 = Fighter(850, 400, 'Bandit', 35, 5, 6, 1, is_enemy = True)
bandit2 = Fighter(700, 420, 'Bandit', 45, 5, 8, 2, is_enemy = True)

# ADD to list
bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)